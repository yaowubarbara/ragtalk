"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Persona } from "@/types";
import { fetchPersonas } from "@/lib/api";
import { getPersonaTheme } from "@/lib/personas";
import ChatInterface from "@/components/ChatInterface";

export default function ChatPage() {
  const params = useParams();
  const personaId = params.personaId as string;
  const [persona, setPersona] = useState<Persona | null>(null);
  const [loading, setLoading] = useState(true);
  const theme = getPersonaTheme(personaId);

  useEffect(() => {
    fetchPersonas()
      .then((personas) => {
        const found = personas.find((p) => p.id === personaId);
        setPersona(found || null);
      })
      .catch(() => setPersona(null))
      .finally(() => setLoading(false));
  }, [personaId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#09090b]">
        <div className="flex flex-col items-center gap-4">
          <div
            className="w-8 h-8 rounded-full border-2 border-t-transparent animate-spin"
            style={{ borderColor: `${theme.primary} transparent ${theme.primary} ${theme.primary}` }}
          />
          <p className="text-white/40 text-sm">Loading...</p>
        </div>
      </div>
    );
  }

  if (!persona) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#09090b]">
        <div className="glass rounded-2xl p-8 text-center max-w-md">
          <h1 className="text-2xl font-bold text-white mb-2">
            Persona not found
          </h1>
          <p className="text-white/40 mb-4">
            The persona you&apos;re looking for doesn&apos;t exist.
          </p>
          <a
            href="/"
            className="inline-block px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            style={{ background: theme.primary, color: "white" }}
          >
            Go back home
          </a>
        </div>
      </div>
    );
  }

  return <ChatInterface persona={persona} />;
}
