import Link from "next/link";
import { Persona } from "@/types";
import { getPersonaTheme } from "@/lib/personas";
import PersonaAvatar from "./PersonaAvatar";

export default function PersonaCard({ persona }: { persona: Persona }) {
  const theme = getPersonaTheme(persona.id);

  return (
    <Link href={`/chat/${persona.id}`} className="group block">
      <div
        className="glass rounded-2xl p-6 transition-all duration-300 cursor-pointer relative overflow-hidden group-hover:scale-[1.02]"
        style={
          {
            "--card-glow": theme.cardGlow,
          } as React.CSSProperties
        }
      >
        {/* Top accent line */}
        <div
          className="absolute top-0 left-0 right-0 h-[2px] opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            background: `linear-gradient(90deg, ${theme.gradientFrom}, ${theme.gradientTo})`,
          }}
        />

        {/* Hover glow */}
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl pointer-events-none"
          style={{
            boxShadow: `0 0 40px ${theme.cardGlow}, inset 0 0 40px ${theme.cardGlow}`,
          }}
        />

        <div className="relative">
          <div className="flex items-center gap-4 mb-4">
            <div
              className="rounded-full p-[2px]"
              style={{
                background: `linear-gradient(135deg, ${theme.gradientFrom}, ${theme.gradientTo})`,
              }}
            >
              <div className="rounded-full bg-[#09090b] p-[2px]">
                <PersonaAvatar personaId={persona.id} size={56} />
              </div>
            </div>
            <div className="flex-1">
              <h2 className="text-lg font-semibold text-white">
                {persona.name}
              </h2>
              <p className="text-sm text-white/40">{persona.title}</p>
            </div>
            <span className="text-white/20 group-hover:text-white/60 group-hover:translate-x-1 transition-all duration-300">
              &rarr;
            </span>
          </div>

          <p className="text-white/50 text-sm leading-relaxed mb-3">
            {persona.description}
          </p>

          <span
            className="inline-block text-xs px-3 py-1 rounded-full"
            style={{
              background: `${theme.primary}20`,
              color: theme.secondary,
            }}
          >
            {theme.shortDescription}
          </span>
        </div>
      </div>
    </Link>
  );
}
