import { PersonaTheme } from "@/lib/personas";

// Munger: Matrix-style data grid - rational thinking / mental models
function MungerBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      {/* Floating grid lines */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.04]">
        <defs>
          <pattern id="munger-grid" width="60" height="60" patternUnits="userSpaceOnUse">
            <path d="M60 0V60H0" fill="none" stroke={theme.secondary} strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#munger-grid)" />
      </svg>
      {/* Data stream columns */}
      <div className="absolute inset-0 overflow-hidden opacity-[0.03]">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute top-0 text-[10px] font-mono leading-4 animate-data-fall"
            style={{
              left: `${12 + i * 12}%`,
              color: theme.secondary,
              animationDelay: `${i * 1.7}s`,
              animationDuration: `${12 + i * 2}s`,
            }}
          >
            {[...Array(30)].map((_, j) => (
              <div key={j}>{(Math.random() * 100).toFixed(2)}</div>
            ))}
          </div>
        ))}
      </div>
      {/* Gradient orbs */}
      <div className="absolute top-[20%] right-[10%] w-[400px] h-[400px] rounded-full blur-[140px] opacity-[0.06]"
        style={{ background: theme.primary }} />
      <div className="absolute bottom-[10%] left-[5%] w-[300px] h-[300px] rounded-full blur-[120px] opacity-[0.04]"
        style={{ background: theme.secondary }} />
    </>
  );
}

// Franklin: Circuit board + lightning arcs - electricity / invention
function FranklinBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      {/* Circuit board pattern */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.04]">
        <defs>
          <pattern id="franklin-circuit" width="80" height="80" patternUnits="userSpaceOnUse">
            <circle cx="40" cy="40" r="2" fill={theme.secondary} />
            <circle cx="0" cy="0" r="2" fill={theme.secondary} />
            <circle cx="80" cy="0" r="2" fill={theme.secondary} />
            <circle cx="0" cy="80" r="2" fill={theme.secondary} />
            <circle cx="80" cy="80" r="2" fill={theme.secondary} />
            <path d="M0 0h20v40h20M80 0h-20v40h-20M0 80h20v-40h20M80 80h-20v-40h-20" fill="none" stroke={theme.secondary} strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#franklin-circuit)" />
      </svg>
      {/* Lightning bolts */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.06]">
        <path d="M200 0 L185 120 L210 120 L180 280" fill="none" stroke={theme.secondary} strokeWidth="1" className="animate-lightning" />
        <path d="M600 0 L580 100 L610 100 L575 250" fill="none" stroke={theme.primary} strokeWidth="1" className="animate-lightning-delayed" />
      </svg>
      {/* Glow orbs */}
      <div className="absolute top-[10%] left-[20%] w-[500px] h-[500px] rounded-full blur-[160px] opacity-[0.05]"
        style={{ background: theme.secondary }} />
      <div className="absolute bottom-[20%] right-[15%] w-[350px] h-[350px] rounded-full blur-[120px] opacity-[0.04]"
        style={{ background: theme.primary }} />
    </>
  );
}

// Aurelius: Star constellation / cosmos - stoic contemplation
function AureliusBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      {/* Star field */}
      <div className="absolute inset-0 overflow-hidden">
        {[...Array(40)].map((_, i) => (
          <div
            key={i}
            className="absolute rounded-full animate-twinkle"
            style={{
              width: i % 3 === 0 ? 2 : 1,
              height: i % 3 === 0 ? 2 : 1,
              left: `${(i * 37 + 13) % 100}%`,
              top: `${(i * 53 + 7) % 100}%`,
              background: i % 2 === 0 ? theme.secondary : "#ffffff",
              animationDelay: `${(i * 0.3) % 4}s`,
              animationDuration: `${3 + (i % 3)}s`,
            }}
          />
        ))}
      </div>
      {/* Constellation lines */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.03]">
        <line x1="10%" y1="15%" x2="25%" y2="30%" stroke={theme.secondary} strokeWidth="0.5" />
        <line x1="25%" y1="30%" x2="40%" y2="20%" stroke={theme.secondary} strokeWidth="0.5" />
        <line x1="40%" y1="20%" x2="55%" y2="35%" stroke={theme.secondary} strokeWidth="0.5" />
        <line x1="60%" y1="60%" x2="75%" y2="50%" stroke={theme.secondary} strokeWidth="0.5" />
        <line x1="75%" y1="50%" x2="85%" y2="70%" stroke={theme.secondary} strokeWidth="0.5" />
        <line x1="85%" y1="70%" x2="70%" y2="80%" stroke={theme.secondary} strokeWidth="0.5" />
      </svg>
      {/* Nebula */}
      <div className="absolute top-[30%] left-[40%] w-[500px] h-[500px] rounded-full blur-[180px] opacity-[0.06] animate-nebula"
        style={{ background: theme.primary }} />
      <div className="absolute top-[50%] right-[20%] w-[400px] h-[400px] rounded-full blur-[150px] opacity-[0.04] animate-nebula-slow"
        style={{ background: theme.secondary }} />
    </>
  );
}

// Buffett: Stock chart / candlesticks - investing
function BuffettBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      {/* Horizontal guide lines */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.03]">
        {[...Array(10)].map((_, i) => (
          <line key={i} x1="0" y1={`${10 + i * 9}%`} x2="100%" y2={`${10 + i * 9}%`}
            stroke={theme.secondary} strokeWidth="0.3" strokeDasharray="4 8" />
        ))}
      </svg>
      {/* Rising chart line */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.05]" preserveAspectRatio="none" viewBox="0 0 1000 600">
        <defs>
          <linearGradient id="buffett-line-grad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={theme.primary} stopOpacity="0" />
            <stop offset="30%" stopColor={theme.primary} stopOpacity="1" />
            <stop offset="100%" stopColor={theme.secondary} stopOpacity="1" />
          </linearGradient>
          <linearGradient id="buffett-fill-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={theme.secondary} stopOpacity="0.15" />
            <stop offset="100%" stopColor={theme.secondary} stopOpacity="0" />
          </linearGradient>
        </defs>
        <path d="M0 450 Q100 440 200 400 T400 350 T600 280 T800 180 T1000 100"
          fill="none" stroke="url(#buffett-line-grad)" strokeWidth="2" className="animate-chart-draw" />
        <path d="M0 450 Q100 440 200 400 T400 350 T600 280 T800 180 T1000 100 V600 H0 Z"
          fill="url(#buffett-fill-grad)" className="animate-chart-draw" />
      </svg>
      {/* Candlesticks */}
      <div className="absolute inset-0 opacity-[0.04] flex items-end justify-around px-[10%] pb-[15%]">
        {[65, 50, 70, 45, 80, 55, 90, 60, 75, 85, 50, 95, 70, 80].map((h, i) => (
          <div key={i} className="flex flex-col items-center">
            <div
              className="w-[2px] rounded-full"
              style={{
                height: `${h * 0.7}px`,
                background: h > 60 ? theme.secondary : theme.primary,
              }}
            />
          </div>
        ))}
      </div>
      <div className="absolute bottom-[15%] right-[10%] w-[400px] h-[300px] rounded-full blur-[140px] opacity-[0.05]"
        style={{ background: theme.secondary }} />
    </>
  );
}

// Confucius: Flowing concentric circles + geometric harmony
function ConfuciusBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      {/* Concentric circles - harmony */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.04]">
        <defs>
          <radialGradient id="confucius-fade" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor={theme.secondary} stopOpacity="1" />
            <stop offset="100%" stopColor={theme.secondary} stopOpacity="0" />
          </radialGradient>
        </defs>
        {[...Array(8)].map((_, i) => (
          <circle key={i} cx="50%" cy="45%" r={`${8 + i * 6}%`}
            fill="none" stroke={theme.secondary} strokeWidth="0.3"
            className="animate-ripple" style={{ animationDelay: `${i * 0.5}s` }} />
        ))}
      </svg>
      {/* Flowing ink strokes */}
      <svg className="absolute inset-0 w-full h-full opacity-[0.03]" viewBox="0 0 1000 800">
        <path d="M100 400 Q250 200 400 350 T700 300 T950 250"
          fill="none" stroke={theme.secondary} strokeWidth="1.5" strokeLinecap="round"
          className="animate-brush-stroke" />
        <path d="M50 500 Q200 600 450 450 T800 500"
          fill="none" stroke={theme.primary} strokeWidth="1" strokeLinecap="round"
          className="animate-brush-stroke-delayed" />
      </svg>
      {/* Warm glow */}
      <div className="absolute top-[25%] left-[35%] w-[450px] h-[450px] rounded-full blur-[160px] opacity-[0.06]"
        style={{ background: theme.secondary }} />
      <div className="absolute bottom-[20%] right-[25%] w-[350px] h-[350px] rounded-full blur-[140px] opacity-[0.04]"
        style={{ background: theme.primary }} />
    </>
  );
}

// Naval: Network mesh / interconnected nodes - leverage & connections
function NavalBg({ theme }: { theme: PersonaTheme }) {
  const nodes = [
    { x: 15, y: 20 }, { x: 35, y: 15 }, { x: 55, y: 25 }, { x: 75, y: 12 }, { x: 90, y: 28 },
    { x: 10, y: 45 }, { x: 30, y: 50 }, { x: 50, y: 42 }, { x: 70, y: 48 }, { x: 85, y: 55 },
    { x: 20, y: 70 }, { x: 40, y: 75 }, { x: 60, y: 68 }, { x: 80, y: 72 }, { x: 95, y: 80 },
    { x: 5, y: 85 }, { x: 45, y: 90 }, { x: 65, y: 88 },
  ];
  const edges = [
    [0, 1], [1, 2], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8], [8, 9],
    [10, 11], [11, 12], [12, 13], [13, 14], [0, 5], [1, 6], [2, 7],
    [3, 8], [4, 9], [5, 10], [6, 11], [7, 12], [8, 13], [9, 14],
    [10, 15], [11, 16], [12, 16], [13, 17], [15, 16], [16, 17],
  ];

  return (
    <>
      {/* Network mesh */}
      <svg className="absolute inset-0 w-full h-full">
        {/* Edges */}
        {edges.map(([a, b], i) => (
          <line key={`e${i}`}
            x1={`${nodes[a].x}%`} y1={`${nodes[a].y}%`}
            x2={`${nodes[b].x}%`} y2={`${nodes[b].y}%`}
            stroke={theme.secondary} strokeWidth="0.5" opacity="0.04"
            className="animate-network-pulse"
            style={{ animationDelay: `${(i * 0.3) % 5}s` }}
          />
        ))}
        {/* Nodes */}
        {nodes.map((n, i) => (
          <circle key={`n${i}`}
            cx={`${n.x}%`} cy={`${n.y}%`}
            r={i % 4 === 0 ? "3" : "2"}
            fill={theme.secondary} opacity="0.06"
            className="animate-twinkle"
            style={{ animationDelay: `${(i * 0.4) % 3}s` }}
          />
        ))}
        {/* Data packets traveling along edges */}
        {[0, 3, 7, 12, 18].map((edgeIdx) => {
          const [a, b] = edges[edgeIdx];
          return (
            <circle key={`p${edgeIdx}`} r="2" fill={theme.secondary} opacity="0.15">
              <animateMotion
                dur={`${3 + edgeIdx % 3}s`}
                repeatCount="indefinite"
                path={`M${nodes[a].x * 10} ${nodes[a].y * 8} L${nodes[b].x * 10} ${nodes[b].y * 8}`}
              />
            </circle>
          );
        })}
      </svg>
      {/* Glow */}
      <div className="absolute top-[15%] left-[30%] w-[500px] h-[500px] rounded-full blur-[180px] opacity-[0.05]"
        style={{ background: theme.primary }} />
      <div className="absolute bottom-[10%] right-[20%] w-[400px] h-[400px] rounded-full blur-[140px] opacity-[0.04]"
        style={{ background: theme.secondary }} />
    </>
  );
}

// Default fallback
function DefaultBg({ theme }: { theme: PersonaTheme }) {
  return (
    <>
      <div className="absolute top-[20%] left-[30%] w-[400px] h-[400px] rounded-full blur-[150px] opacity-[0.05]"
        style={{ background: theme.primary }} />
      <div className="absolute bottom-[20%] right-[20%] w-[300px] h-[300px] rounded-full blur-[120px] opacity-[0.04]"
        style={{ background: theme.secondary }} />
    </>
  );
}

const backgroundMap: Record<string, React.FC<{ theme: PersonaTheme }>> = {
  "charlie-munger": MungerBg,
  "benjamin-franklin": FranklinBg,
  "marcus-aurelius": AureliusBg,
  "warren-buffett": BuffettBg,
  confucius: ConfuciusBg,
  "naval-ravikant": NavalBg,
};

export default function ChatBackground({
  personaId,
  theme,
}: {
  personaId: string;
  theme: PersonaTheme;
}) {
  const Bg = backgroundMap[personaId] || DefaultBg;
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      <Bg theme={theme} />
    </div>
  );
}
