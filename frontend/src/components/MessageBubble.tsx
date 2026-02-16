"use client";

import { useState } from "react";
import { ChatMessage, Citation } from "@/types";
import { PersonaTheme } from "@/lib/personas";
import PersonaAvatar from "./PersonaAvatar";

function CitationBadge({
  citation,
  theme,
  isExpanded,
  onClick,
}: {
  citation: Citation;
  theme: PersonaTheme;
  isExpanded: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className="inline-flex items-center gap-1 text-[10px] px-2 py-0.5 rounded-full transition-all hover:scale-105"
      style={{
        background: `${theme.primary}30`,
        color: theme.secondary,
        border: `1px solid ${theme.primary}40`,
      }}
    >
      <span className="font-mono font-bold">[{citation.id}]</span>
      <span className="opacity-70">{citation.source}</span>
    </button>
  );
}

function SourcesPanel({
  sources,
  theme,
}: {
  sources: Citation[];
  theme: PersonaTheme;
}) {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  return (
    <div className="mt-2 pt-2 border-t border-white/[0.06]">
      <p className="text-[10px] uppercase tracking-wider opacity-40 mb-1.5">
        Sources
      </p>
      <div className="flex flex-wrap gap-1.5">
        {sources.map((s) => (
          <div key={s.id} className="relative">
            <CitationBadge
              citation={s}
              theme={theme}
              isExpanded={expandedId === s.id}
              onClick={() =>
                setExpandedId(expandedId === s.id ? null : s.id)
              }
            />
            {expandedId === s.id && (
              <div
                className="absolute bottom-full left-0 mb-1 w-64 p-2 rounded-lg text-[11px] leading-relaxed z-10 glass-strong"
                style={{ color: theme.bubbleText }}
              >
                <p className="opacity-50 text-[9px] mb-1">
                  {s.source} &middot; {s.doc_type}
                </p>
                <p>{s.text}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

/**
 * Render message content with inline citation highlights.
 * Matches [1], [2], etc. in the text and styles them as badges.
 */
function renderContentWithCitations(
  content: string,
  theme: PersonaTheme
) {
  const parts = content.split(/(\[\d+\])/g);
  return parts.map((part, i) => {
    const match = part.match(/^\[(\d+)\]$/);
    if (match) {
      return (
        <span
          key={i}
          className="inline-flex items-center text-[10px] font-mono font-bold px-1 py-0 rounded mx-0.5 align-baseline"
          style={{
            background: `${theme.primary}30`,
            color: theme.secondary,
          }}
        >
          {part}
        </span>
      );
    }
    return <span key={i}>{part}</span>;
  });
}

export default function MessageBubble({
  message,
  personaName,
  theme,
  personaId,
}: {
  message: ChatMessage;
  personaName: string;
  theme: PersonaTheme;
  personaId: string;
}) {
  const isUser = message.role === "user";
  const isEmpty = !isUser && message.content === "";
  const hasSources = !isUser && message.sources && message.sources.length > 0;

  return (
    <div
      className={`flex ${isUser ? "justify-end animate-slide-in-right" : "justify-start animate-slide-in-left"} mb-4`}
    >
      {!isUser && (
        <div className="mr-3 mt-1 flex-shrink-0">
          <PersonaAvatar personaId={personaId} size={32} />
        </div>
      )}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-white/10 text-white rounded-br-md"
            : "rounded-bl-md"
        }`}
        style={
          !isUser
            ? { background: theme.bubbleBg, color: theme.bubbleText }
            : undefined
        }
      >
        {!isUser && (
          <p className="text-xs font-medium mb-1 opacity-60">
            {personaName}
          </p>
        )}
        {isEmpty ? (
          <div className="flex items-center gap-1.5 py-1 text-white/50">
            <span className="typing-dot" />
            <span className="typing-dot" />
            <span className="typing-dot" />
          </div>
        ) : (
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {!isUser
              ? renderContentWithCitations(message.content, theme)
              : message.content}
          </p>
        )}
        {hasSources && (
          <SourcesPanel sources={message.sources!} theme={theme} />
        )}
      </div>
    </div>
  );
}
