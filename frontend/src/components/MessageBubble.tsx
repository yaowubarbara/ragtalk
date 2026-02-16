import { ChatMessage } from "@/types";
import { PersonaTheme } from "@/lib/personas";
import PersonaAvatar from "./PersonaAvatar";

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
            {message.content}
          </p>
        )}
      </div>
    </div>
  );
}
