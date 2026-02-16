# RAG Talk - Converse with History's Greatest Minds

[English](#english) | [中文](#中文)

---

<a id="english"></a>

## Overview

A full-stack RAG (Retrieval-Augmented Generation) application that lets you have real-time conversations with AI personas of historical figures. Each response is grounded in actual quotes, writings, and teachings scraped from primary sources, then retrieved via semantic search at query time.

**Live personas:** Charlie Munger, Benjamin Franklin, Marcus Aurelius, Warren Buffett, Confucius, Naval Ravikant

![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![ChromaDB](https://img.shields.io/badge/ChromaDB-0.6-orange)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss)

## Architecture

```
┌─────────────┐     SSE Stream      ┌──────────────┐     Cosine Search    ┌───────────┐
│   Next.js   │ ◄──────────────────► │   FastAPI    │ ◄──────────────────► │ ChromaDB  │
│  Frontend   │     POST /api/chat   │   Backend    │     Top-K Retrieval  │  Vectors  │
└─────────────┘                      └──────┬───────┘                      └───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │  OpenRouter   │
                                     │  LLM API      │
                                     └──────────────┘
```

### Advanced RAG Pipeline

```
User Query
    │
    ▼
┌──────────────────┐
│  Query Rewriter   │  LLM rewrites conversational query → retrieval-optimized form
│  + HyDE           │  Generates hypothetical answer for better embedding match
└────────┬─────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│  BM25  │ │ChromaDB│  Sparse (keyword) + Dense (embedding) retrieval
│ Sparse │ │ Dense  │
└───┬────┘ └───┬────┘
    │          │
    ▼          ▼
┌──────────────────┐
│   RRF Fusion     │  Reciprocal Rank Fusion merges both ranked lists
│  (k=60)          │  without score normalization
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Cross-Encoder   │  Reranks top-20 candidates → top-5
│  Reranker        │  Local model or LLM-as-judge fallback
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Context Builder  │  Numbered citations [1], [2]... with source metadata
│ + Citation IDs   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  LLM Generation  │  Streams response with inline [N] citations
│  (SSE Stream)    │  Sources metadata sent at end of stream
└──────────────────┘
```

Each pipeline stage is **independently toggleable** via environment config:
- `ENABLE_QUERY_REWRITE=true/false`
- `ENABLE_HYBRID_SEARCH=true/false`
- `ENABLE_RERANKER=true/false`

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 16, React 19, TypeScript 5 | UI with real-time SSE streaming |
| Styling | Tailwind CSS 4 | Dark theme, glass morphism, per-persona theming |
| Backend | FastAPI, Uvicorn | Async API with SSE streaming |
| Vector DB | ChromaDB | Dense retrieval with cosine similarity |
| Keyword Search | rank-bm25 | Sparse retrieval for exact keyword matching |
| Reranker | Cross-encoder / LLM-as-judge | Fine-grained relevance scoring |
| LLM | OpenRouter API (Llama 3.1 8B default) | Generation, query rewriting, reranking |
| Scraping | BeautifulSoup4, PyPDF, httpx | Data collection from primary sources |

## Features

- **Hybrid Search** - BM25 keyword + embedding dense retrieval fused via Reciprocal Rank Fusion
- **Cross-Encoder Reranking** - local model (sentence-transformers) with LLM-as-judge fallback
- **Query Rewriting + HyDE** - LLM optimizes queries for retrieval; Hypothetical Document Embeddings for semantic matching
- **Citation System** - numbered `[1]` `[2]` inline references with clickable source badges
- **RAG Evaluation** - LLM-as-Judge pipeline scoring context relevance, faithfulness, and answer relevancy
- **Semantic Chunking** - paragraph-aware splitting with sentence overlap (not naive fixed-size)
- **6 unique AI personas** with distinct personalities, system prompts, and visual themes
- **Real-time streaming** - token-by-token SSE for responsive conversation
- **Per-persona themed UI** - unique animated backgrounds, CSS art avatars, glass morphism
- **Full conversation memory** - history passed to maintain multi-turn context
- **Data pipeline** - automated scraping, cleaning, chunking, and vector ingestion
- **Feature flags** - each pipeline stage independently toggleable

## Data Sources

| Persona | Sources | Content |
|---------|---------|---------|
| Charlie Munger | FS Blog, 25iq.com | Speeches, mental models, quotes |
| Benjamin Franklin | Project Gutenberg | Autobiography, Poor Richard's Almanack |
| Marcus Aurelius | Project Gutenberg | Meditations |
| Warren Buffett | Multiple financial blogs | Shareholder letters, interviews, quotes |
| Confucius | Project Gutenberg | Analerta, teachings |
| Naval Ravikant | Navalmanack | Wealth & happiness principles |

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- An [OpenRouter](https://openrouter.ai/) API key

### 1. Install dependencies
```bash
make setup
```

### 2. Configure environment
```bash
cp .env.example backend/.env
```

Edit `backend/.env`:
```
OPENROUTER_API_KEY=your-key-here
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
CHROMA_DB_PATH=./chroma_db
```

### 3. Build the knowledge base
```bash
make data    # scrape sources + ingest into ChromaDB
```

### 4. Run development servers

Terminal 1:
```bash
make backend    # FastAPI on http://localhost:8000
```

Terminal 2:
```bash
make frontend   # Next.js on http://localhost:3000
```

### 5. Open the app
- Frontend: http://localhost:3000
- API docs: http://localhost:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/personas` | List all available personas |
| `POST` | `/api/chat` | Send message, receive SSE stream |

**Chat request body:**
```json
{
  "persona_id": "charlie-munger",
  "message": "What are mental models?",
  "conversation_history": []
}
```

**SSE response format:**
```
data: {"token": "Mental"}
data: {"token": " models"}
data: {"token": " are"}
...
data: [DONE]
```

## RAG Evaluation

Built-in evaluation pipeline using LLM-as-Judge to measure retrieval and generation quality:

```bash
make evaluate                           # Evaluate all personas
cd backend && python3 -m evaluation.evaluate --persona charlie-munger --verbose
```

Scores three dimensions per query:
| Metric | What it measures |
|--------|-----------------|
| **Context Relevance** | Are the retrieved documents relevant to the query? |
| **Faithfulness** | Is the answer grounded in the retrieved context (not hallucinated)? |
| **Answer Relevancy** | Does the answer actually address the user's question? |

Results are saved to `backend/evaluation/results.json` for tracking over time.

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, routes
│   │   ├── config.py              # Pydantic settings
│   │   ├── models/schemas.py      # Request/response models
│   │   ├── routers/
│   │   │   ├── chat.py            # POST /api/chat (SSE)
│   │   │   └── personas.py        # GET /api/personas
│   │   ├── services/
│   │   │   ├── rag.py             # RAG pipeline & context building
│   │   │   ├── llm.py             # OpenRouter streaming client
│   │   │   └── vectorstore.py     # ChromaDB wrapper
│   │   └── personas/*.json        # Persona definitions
│   ├── scrapers/                  # Web scrapers per source
│   ├── ingestion/                 # Clean, chunk, vectorize pipeline
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                   # Next.js pages & layout
│   │   ├── components/            # React components
│   │   │   ├── ChatInterface.tsx   # Main chat view
│   │   │   ├── ChatBackground.tsx  # Per-persona animated backgrounds
│   │   │   ├── PersonaAvatar.tsx   # CSS art SVG avatars
│   │   │   ├── PersonaCard.tsx     # Homepage persona cards
│   │   │   ├── MessageBubble.tsx   # Chat message bubbles
│   │   │   └── ChatInput.tsx       # Message input bar
│   │   ├── lib/
│   │   │   ├── api.ts             # API client & SSE handler
│   │   │   └── personas.ts        # Theme config & SVG paths
│   │   └── hooks/useChat.ts       # Chat state management
│   └── package.json
├── Makefile                       # Build & run commands
└── .env.example
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install Python + Node dependencies |
| `make scrape` | Scrape all data sources |
| `make ingest` | Ingest scraped data into ChromaDB |
| `make data` | Scrape + ingest (full pipeline) |
| `make backend` | Start FastAPI dev server |
| `make frontend` | Start Next.js dev server |
| `make evaluate` | Run RAG evaluation (LLM-as-Judge) |

---

<a id="中文"></a>

## 概述

一个全栈 RAG（检索增强生成）应用，让你与历史伟人的 AI 人格进行实时对话。每个回复都基于从原始资料中抓取的真实引言、著作和教导，通过语义搜索在查询时检索相关内容。

**内置人物：** 查理·芒格、本杰明·富兰克林、马可·奥勒留、沃伦·巴菲特、孔子、纳瓦尔·拉维坎特

## 架构

```
┌─────────────┐     SSE 流式传输     ┌──────────────┐     余弦相似度搜索    ┌───────────┐
│   Next.js   │ ◄──────────────────► │   FastAPI    │ ◄──────────────────► │ ChromaDB  │
│    前端      │   POST /api/chat    │    后端       │     Top-K 检索      │  向量数据库 │
└─────────────┘                      └──────┬───────┘                      └───────────┘
                                            │
                                            ▼
                                     ┌──────────────┐
                                     │  OpenRouter   │
                                     │  大语言模型    │
                                     └──────────────┘
```

**高级 RAG 流水线：**
1. **Query Rewriting** — LLM 将口语化问题改写为检索优化的查询，支持 HyDE（假设文档嵌入）
2. **混合检索** — BM25 关键词搜索 + ChromaDB 向量搜索并行执行
3. **RRF 融合** — 使用 Reciprocal Rank Fusion 合并两路检索结果（无需分数归一化）
4. **Cross-Encoder 重排序** — 对 Top-20 候选文档精排，输出 Top-5（本地模型优先，LLM 兜底）
5. **引用标注** — 上下文注入编号 `[1]` `[2]`，LLM 生成时自然引用
6. **流式生成** — 逐 token SSE 推送 + 流末尾发送引用源元数据

每个阶段可通过环境变量独立开关：`ENABLE_QUERY_REWRITE`、`ENABLE_HYBRID_SEARCH`、`ENABLE_RERANKER`

## 技术栈

| 层级 | 技术 | 用途 |
|------|------|------|
| 前端 | Next.js 16、React 19、TypeScript 5 | 界面与实时 SSE 流式传输 |
| 样式 | Tailwind CSS 4 | 暗色主题、毛玻璃效果、人物主题定制 |
| 后端 | FastAPI、Uvicorn | 异步 API 与 SSE 流式传输 |
| 向量库 | ChromaDB | 稠密检索（余弦相似度） |
| 关键词搜索 | rank-bm25 | 稀疏检索（精确关键词匹配） |
| 重排序 | Cross-encoder / LLM-as-judge | 细粒度相关性评分 |
| 大模型 | OpenRouter API（默认 Llama 3.1 8B） | 生成、查询改写、重排序 |
| 数据采集 | BeautifulSoup4、PyPDF、httpx | 从原始来源采集数据 |

## 功能特性

- **混合检索** — BM25 关键词 + 向量稠密检索，RRF 融合排序
- **Cross-Encoder 重排序** — 本地模型优先（sentence-transformers），LLM-as-judge 兜底
- **Query Rewriting + HyDE** — LLM 优化查询；假设文档嵌入提升语义匹配
- **引用系统** — 行内 `[1]` `[2]` 编号引用，可点击查看原始来源
- **RAG 评估** — LLM-as-Judge 流水线，评分上下文相关性、忠实度、回答相关性
- **语义分块** — 段落感知切分 + 句子重叠（非固定字符数硬切）
- **6 个独特 AI 人物** — 各有独立性格、系统提示词和视觉主题
- **实时流式传输** — 逐 token SSE 推送，对话响应即时
- **人物专属主题 UI** — 独特动画背景、CSS 艺术头像、毛玻璃效果
- **完整对话记忆** — 传递历史记录以维持多轮对话上下文
- **数据管线** — 自动化抓取、清洗、分块与向量化入库
- **功能开关** — 每个流水线阶段可独立启停

## 数据来源

| 人物 | 来源 | 内容 |
|------|------|------|
| 查理·芒格 | FS Blog、25iq.com | 演讲、思维模型、语录 |
| 本杰明·富兰克林 | Project Gutenberg | 自传、穷理查年鉴 |
| 马可·奥勒留 | Project Gutenberg | 沉思录 |
| 沃伦·巴菲特 | 多个金融博客 | 致股东信、访谈、语录 |
| 孔子 | Project Gutenberg | 论语、学说 |
| 纳瓦尔·拉维坎特 | Navalmanack | 财富与幸福原则 |

## 快速开始

### 前置要求
- Python 3.10+
- Node.js 18+
- [OpenRouter](https://openrouter.ai/) API 密钥

### 1. 安装依赖
```bash
make setup
```

### 2. 配置环境变量
```bash
cp .env.example backend/.env
```

编辑 `backend/.env`：
```
OPENROUTER_API_KEY=你的密钥
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
CHROMA_DB_PATH=./chroma_db
```

### 3. 构建知识库
```bash
make data    # 抓取数据源 + 入库 ChromaDB
```

### 4. 启动开发服务器

终端 1：
```bash
make backend    # FastAPI 运行在 http://localhost:8000
```

终端 2：
```bash
make frontend   # Next.js 运行在 http://localhost:3000
```

### 5. 打开应用
- 前端：http://localhost:3000
- API 文档：http://localhost:8000/docs

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/health` | 健康检查 |
| `GET` | `/api/personas` | 获取所有可用人物 |
| `POST` | `/api/chat` | 发送消息，接收 SSE 流 |

## Make 命令

| 命令 | 说明 |
|------|------|
| `make setup` | 安装 Python + Node 依赖 |
| `make scrape` | 抓取所有数据源 |
| `make ingest` | 将抓取数据导入 ChromaDB |
| `make data` | 抓取 + 导入（完整管线） |
| `make backend` | 启动 FastAPI 开发服务器 |
| `make frontend` | 启动 Next.js 开发服务器 |
| `make evaluate` | 运行 RAG 评估（LLM-as-Judge） |
