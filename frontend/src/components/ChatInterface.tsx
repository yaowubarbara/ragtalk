"use client";

import { useEffect, useRef } from "react";
import { Persona } from "@/types";
import { getPersonaTheme } from "@/lib/personas";
import { useChat } from "@/hooks/useChat";
import PersonaAvatar from "./PersonaAvatar";
import ChatBackground from "./ChatBackground";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";

export default function ChatInterface({ persona }: { persona: Persona }) {
  const { messages, isStreaming, error, sendMessage } = useChat(persona.id);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const theme = getPersonaTheme(persona.id);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-[#09090b]">
      {/* Header */}
      <div
        className="border-b border-white/[0.06] px-6 py-4 flex items-center gap-3 backdrop-blur-xl"
        style={{ background: theme.headerBg }}
      >
        <a
          href="/"
          className="text-white/40 hover:text-white/80 mr-2 transition-colors"
        >
          &larr;
        </a>
        <div
          className="rounded-full p-[2px]"
          style={{
            background: `linear-gradient(135deg, ${theme.gradientFrom}, ${theme.gradientTo})`,
          }}
        >
          <div className="rounded-full bg-[#09090b] p-[2px]">
            <PersonaAvatar personaId={persona.id} size={40} />
          </div>
        </div>
        <div>
          <h1
            className="text-lg font-semibold"
            style={{ color: theme.headerText }}
          >
            {persona.name}
          </h1>
          <p className="text-xs text-white/50">{persona.title}</p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-4 relative">
        {/* Per-persona background */}
        <ChatBackground personaId={persona.id} theme={theme} />
        <div className="max-w-3xl mx-auto relative">
          {/* Greeting */}
          <MessageBubble
            message={{ role: "assistant", content: persona.greeting }}
            personaName={persona.name}
            theme={theme}
            personaId={persona.id}
          />

          {messages.map((msg, i) => (
            <MessageBubble
              key={i}
              message={msg}
              personaName={persona.name}
              theme={theme}
              personaId={persona.id}
            />
          ))}

          {error && (
            <div className="text-center text-red-400 text-sm py-2">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isStreaming} theme={theme} />
    </div>
  );
}
