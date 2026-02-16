import { getPersonaTheme } from "@/lib/personas";

export default function PersonaAvatar({
  personaId,
  size = 48,
}: {
  personaId: string;
  size?: number;
}) {
  const theme = getPersonaTheme(personaId);
  const iconSize = size * 0.5;
  const iconOffset = (size - iconSize) / 2;

  return (
    <div
      className="rounded-full flex-shrink-0 relative"
      style={{
        width: size,
        height: size,
        background: `linear-gradient(135deg, ${theme.gradientFrom}, ${theme.gradientTo})`,
      }}
    >
      <svg
        width={iconSize}
        height={iconSize}
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        style={{
          position: "absolute",
          top: iconOffset,
          left: iconOffset,
        }}
      >
        <path
          d={theme.iconPath}
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill="none"
        />
      </svg>
    </div>
  );
}
