"use client";

import { useEffect, useState } from "react";
import { Persona } from "@/types";
import { fetchPersonas } from "@/lib/api";
import PersonaCard from "@/components/PersonaCard";

const techStack = ["Next.js", "FastAPI", "ChromaDB", "RAG", "SSE"];

export default function Home() {
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPersonas()
      .then(setPersonas)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="min-h-screen bg-[#09090b] relative overflow-hidden">
      {/* Ambient gradient orbs */}
      <div className="pointer-events-none absolute inset-0 overflow-hidden">
        <div className="absolute -top-[400px] -left-[300px] w-[800px] h-[800px] rounded-full bg-purple-500/[0.07] blur-[120px]" />
        <div className="absolute -top-[200px] -right-[300px] w-[600px] h-[600px] rounded-full bg-cyan-500/[0.05] blur-[120px]" />
        <div className="absolute top-[60%] left-[50%] -translate-x-1/2 w-[800px] h-[400px] rounded-full bg-blue-500/[0.04] blur-[120px]" />
      </div>

      {/* Dot grid */}
      <div className="absolute inset-0 bg-grid-pattern pointer-events-none" />

      <div className="relative max-w-6xl mx-auto px-6">
        {/* Nav */}
        <nav className="flex items-center justify-between py-6">
          <span className="text-white/80 font-semibold text-lg tracking-tight">
            AI Talk With You
          </span>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-white/30 hover:text-white/60 transition-colors text-sm"
          >
            GitHub
          </a>
        </nav>

        {/* Hero */}
        <div className="text-center pt-16 pb-20">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass text-xs text-white/60 mb-6">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            Portfolio Project
          </div>

          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight mb-6 gradient-text leading-tight">
            Converse with
            <br />
            History&apos;s Greatest Minds
          </h1>

          <p className="text-white/40 text-lg max-w-2xl mx-auto leading-relaxed">
            A RAG-powered AI application that lets you have authentic
            conversations with historical figures, built with retrieval-augmented
            generation and real-time streaming.
          </p>
        </div>

        {/* Persona Grid */}
        {loading && (
          <div className="text-center text-white/30 py-12">
            <div className="w-6 h-6 rounded-full border-2 border-white/20 border-t-white/60 animate-spin mx-auto mb-3" />
            Loading personas...
          </div>
        )}

        {error && (
          <div className="text-center py-12">
            <div className="glass inline-block rounded-xl px-6 py-4">
              <p className="text-red-400 text-sm">
                Failed to load personas. Make sure the backend is running.
              </p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 stagger-children pb-12">
          {personas.map((persona) => (
            <PersonaCard key={persona.id} persona={persona} />
          ))}
        </div>

        {/* Tech Stack Footer */}
        <div className="border-t border-white/[0.06] py-8 mt-8">
          <div className="flex flex-wrap items-center justify-center gap-3">
            <span className="text-white/20 text-xs mr-2">Built with</span>
            {techStack.map((tech) => (
              <span
                key={tech}
                className="text-xs px-3 py-1 rounded-full glass text-white/40"
              >
                {tech}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
