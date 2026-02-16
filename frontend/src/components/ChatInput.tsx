"use client";

import { useState, KeyboardEvent } from "react";
import { PersonaTheme } from "@/lib/personas";

export default function ChatInput({
  onSend,
  disabled,
  theme,
}: {
  onSend: (message: string) => void;
  disabled: boolean;
  theme: PersonaTheme;
}) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
      setInput("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-white/[0.06] bg-[#09090b]/80 backdrop-blur-xl p-4">
      <div className="flex gap-3 max-w-3xl mx-auto">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white placeholder:text-white/30 focus:outline-none focus:ring-2 focus:border-transparent disabled:opacity-50 transition-colors"
          style={
            {
              "--tw-ring-color": theme.inputRingColor,
            } as React.CSSProperties
          }
        />
        <button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          className="px-5 py-3 text-white rounded-xl text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          style={{
            background: disabled || !input.trim() ? undefined : theme.sendButtonBg,
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
