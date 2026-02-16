"use client";

import { useState, useCallback, useRef } from "react";
import { ChatMessage } from "@/types";
import { streamChat } from "@/lib/api";

export function useChat(personaId: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortRef = useRef(false);

  const sendMessage = useCallback(
    async (content: string) => {
      if (isStreaming || !content.trim()) return;

      setError(null);
      abortRef.current = false;

      const userMessage: ChatMessage = { role: "user", content };
      const updatedHistory = [...messages, userMessage];
      setMessages(updatedHistory);
      setIsStreaming(true);

      // Add empty assistant message that we'll stream into
      setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

      await streamChat(
        personaId,
        content,
        // Send the history before this message
        messages,
        // onToken
        (token) => {
          if (abortRef.current) return;
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            updated[updated.length - 1] = {
              ...last,
              content: last.content + token,
            };
            return updated;
          });
        },
        // onDone
        () => {
          setIsStreaming(false);
        },
        // onError
        (err) => {
          setError(err);
          setIsStreaming(false);
        }
      );
    },
    [personaId, messages, isStreaming]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
  }, []);

  return { messages, isStreaming, error, sendMessage, clearMessages };
}
