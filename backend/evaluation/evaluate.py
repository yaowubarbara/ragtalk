"""RAG evaluation pipeline using LLM-as-Judge.

Evaluates three dimensions:
1. Context Relevance - Are the retrieved documents relevant to the query?
2. Faithfulness - Is the generated answer grounded in the retrieved context?
3. Answer Relevancy - Does the answer actually address the user's question?

This is a lightweight alternative to RAGAS that uses the same LLM
(via OpenRouter) as the judge, requiring no additional dependencies.

Usage:
    python -m evaluation.evaluate
    python -m evaluation.evaluate --persona charlie-munger
    python -m evaluation.evaluate --verbose
"""

import asyncio
import json
import argparse
from pathlib import Path

from app.services.rag import retrieve_context, load_persona, build_context_block
from app.services.llm import chat_completion, stream_chat_completion

# Test questions per persona — designed to test different retrieval scenarios
TEST_QUESTIONS: dict[str, list[str]] = {
    "charlie-munger": [
        "What are mental models and why are they important?",
        "What does Munger think about the psychology of human misjudgment?",
        "How should one approach investment decisions?",
        "What is the lollapalooza effect?",
        "What books does Charlie Munger recommend?",
    ],
    "benjamin-franklin": [
        "What are your most important virtues?",
        "Tell me about your experiments with electricity.",
        "What advice do you give about managing money?",
        "What was your daily routine like?",
        "What is the key to self-improvement?",
    ],
    "marcus-aurelius": [
        "How do you deal with adversity?",
        "What is the nature of the universe according to Stoicism?",
        "How should a leader behave?",
        "What is the role of fate in human life?",
        "How do you control your emotions?",
    ],
    "warren-buffett": [
        "What is value investing?",
        "How do you evaluate a company's moat?",
        "What mistakes should investors avoid?",
        "What is your opinion on diversification?",
        "How do you think about risk?",
    ],
    "confucius": [
        "What is the meaning of ren (benevolence)?",
        "How should a ruler govern?",
        "What is the role of education in society?",
        "What is the importance of ritual and propriety?",
        "How should one treat their parents?",
    ],
    "naval-ravikant": [
        "How do you build wealth without getting lucky?",
        "What is specific knowledge?",
        "How do you find happiness?",
        "What is the role of leverage in wealth creation?",
        "Should you follow your passion or develop skills?",
    ],
}


async def score_context_relevance(query: str, contexts: list[str]) -> float:
    """Score how relevant the retrieved contexts are to the query (0-10)."""
    context_text = "\n---\n".join(contexts[:5])
    messages = [
        {
            "role": "system",
            "content": (
                "You are an impartial judge evaluating retrieval quality. "
                "Score how relevant the retrieved documents are to the query. "
                "Output ONLY a number from 0 to 10. "
                "10 = perfectly relevant, 0 = completely irrelevant."
            ),
        },
        {
            "role": "user",
            "content": f"Query: {query}\n\nRetrieved Documents:\n{context_text}\n\nRelevance Score:",
        },
    ]
    response = await chat_completion(messages, temperature=0.0, max_tokens=10)
    try:
        return min(10.0, max(0.0, float(response.strip())))
    except ValueError:
        return 5.0


async def score_faithfulness(answer: str, contexts: list[str]) -> float:
    """Score how grounded the answer is in the retrieved contexts (0-10)."""
    context_text = "\n---\n".join(contexts[:5])
    messages = [
        {
            "role": "system",
            "content": (
                "You are an impartial judge evaluating answer faithfulness. "
                "Score how well the answer is grounded in (supported by) the provided contexts. "
                "Output ONLY a number from 0 to 10. "
                "10 = fully grounded in context, 0 = completely fabricated."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Contexts:\n{context_text}\n\n"
                f"Answer:\n{answer}\n\n"
                "Faithfulness Score:"
            ),
        },
    ]
    response = await chat_completion(messages, temperature=0.0, max_tokens=10)
    try:
        return min(10.0, max(0.0, float(response.strip())))
    except ValueError:
        return 5.0


async def score_answer_relevancy(query: str, answer: str) -> float:
    """Score how well the answer addresses the original question (0-10)."""
    messages = [
        {
            "role": "system",
            "content": (
                "You are an impartial judge evaluating answer quality. "
                "Score how well the answer addresses the user's question. "
                "Output ONLY a number from 0 to 10. "
                "10 = perfectly addresses the question, 0 = completely off-topic."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {query}\n\nAnswer:\n{answer}\n\nRelevancy Score:",
        },
    ]
    response = await chat_completion(messages, temperature=0.0, max_tokens=10)
    try:
        return min(10.0, max(0.0, float(response.strip())))
    except ValueError:
        return 5.0


async def generate_answer(persona_id: str, query: str) -> str:
    """Generate a full answer for evaluation (non-streaming)."""
    from app.services.rag import generate_response
    from app.models.schemas import ChatMessage

    tokens = []
    async for item in generate_response(persona_id, query, []):
        if isinstance(item, str):
            tokens.append(item)
    return "".join(tokens)


async def evaluate_single(
    persona_id: str,
    query: str,
    verbose: bool = False,
) -> dict:
    """Evaluate a single query through the full RAG pipeline."""
    persona = load_persona(persona_id)

    # Retrieve context
    documents, rewritten_query = await retrieve_context(
        persona_id, persona["name"], query
    )
    contexts = [doc["content"] for doc in documents]

    # Generate answer
    answer = await generate_answer(persona_id, query)

    # Score all three dimensions
    ctx_score = await score_context_relevance(query, contexts)
    faith_score = await score_faithfulness(answer, contexts)
    relevancy_score = await score_answer_relevancy(query, answer)

    result = {
        "query": query,
        "rewritten_query": rewritten_query,
        "num_contexts": len(contexts),
        "answer_length": len(answer),
        "context_relevance": ctx_score,
        "faithfulness": faith_score,
        "answer_relevancy": relevancy_score,
        "avg_score": round((ctx_score + faith_score + relevancy_score) / 3, 2),
    }

    if verbose:
        result["answer_preview"] = answer[:200]
        result["context_preview"] = [c[:100] for c in contexts[:3]]

    return result


async def evaluate_persona(persona_id: str, verbose: bool = False) -> dict:
    """Evaluate all test questions for a single persona."""
    questions = TEST_QUESTIONS.get(persona_id, [])
    if not questions:
        return {"persona_id": persona_id, "error": "No test questions defined"}

    print(f"\n{'='*60}")
    print(f"Evaluating: {persona_id}")
    print(f"{'='*60}")

    results = []
    for i, query in enumerate(questions, 1):
        print(f"  [{i}/{len(questions)}] {query[:60]}...")
        result = await evaluate_single(persona_id, query, verbose)
        results.append(result)
        print(
            f"    Context: {result['context_relevance']:.1f} | "
            f"Faithful: {result['faithfulness']:.1f} | "
            f"Relevant: {result['answer_relevancy']:.1f} | "
            f"Avg: {result['avg_score']:.1f}"
        )

    # Aggregate scores
    avg_ctx = sum(r["context_relevance"] for r in results) / len(results)
    avg_faith = sum(r["faithfulness"] for r in results) / len(results)
    avg_rel = sum(r["answer_relevancy"] for r in results) / len(results)

    summary = {
        "persona_id": persona_id,
        "num_questions": len(results),
        "avg_context_relevance": round(avg_ctx, 2),
        "avg_faithfulness": round(avg_faith, 2),
        "avg_answer_relevancy": round(avg_rel, 2),
        "overall_score": round((avg_ctx + avg_faith + avg_rel) / 3, 2),
        "details": results,
    }

    print(f"\n  Summary for {persona_id}:")
    print(f"    Context Relevance:  {avg_ctx:.2f}/10")
    print(f"    Faithfulness:       {avg_faith:.2f}/10")
    print(f"    Answer Relevancy:   {avg_rel:.2f}/10")
    print(f"    Overall:            {summary['overall_score']:.2f}/10")

    return summary


async def run_full_evaluation(
    persona_ids: list[str] | None = None,
    verbose: bool = False,
):
    """Run evaluation across all (or specified) personas."""
    if persona_ids is None:
        persona_ids = list(TEST_QUESTIONS.keys())

    all_results = []
    for pid in persona_ids:
        result = await evaluate_persona(pid, verbose)
        all_results.append(result)

    # Overall summary
    valid = [r for r in all_results if "error" not in r]
    if valid:
        print(f"\n{'='*60}")
        print("OVERALL EVALUATION SUMMARY")
        print(f"{'='*60}")
        overall = sum(r["overall_score"] for r in valid) / len(valid)
        for r in valid:
            print(f"  {r['persona_id']:25s} → {r['overall_score']:.2f}/10")
        print(f"\n  {'Overall Average':25s} → {overall:.2f}/10")

    # Save results
    output_path = Path("evaluation/results.json")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\nDetailed results saved to {output_path}")

    return all_results


def main():
    parser = argparse.ArgumentParser(description="Evaluate RAG pipeline quality")
    parser.add_argument(
        "--persona", type=str, default=None,
        help="Evaluate a specific persona (e.g., charlie-munger)",
    )
    parser.add_argument(
        "--verbose", action="store_true",
        help="Include answer and context previews in output",
    )
    args = parser.parse_args()

    persona_ids = [args.persona] if args.persona else None
    asyncio.run(run_full_evaluation(persona_ids, args.verbose))


if __name__ == "__main__":
    main()
