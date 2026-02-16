export interface PersonaTheme {
  id: string;
  primary: string;
  secondary: string;
  gradientFrom: string;
  gradientTo: string;
  bubbleBg: string;
  bubbleText: string;
  headerBg: string;
  headerText: string;
  cardGlow: string;
  inputRingColor: string;
  sendButtonBg: string;
  sendButtonHover: string;
  shortDescription: string;
  iconPath: string;
}

const personaThemes: Record<string, PersonaTheme> = {
  "charlie-munger": {
    id: "charlie-munger",
    primary: "#1e3a5f",
    secondary: "#d4a84b",
    gradientFrom: "#1e3a5f",
    gradientTo: "#d4a84b",
    bubbleBg: "rgba(30, 58, 95, 0.3)",
    bubbleText: "#e2e8f0",
    headerBg: "rgba(30, 58, 95, 0.8)",
    headerText: "#d4a84b",
    cardGlow: "rgba(30, 58, 95, 0.4)",
    inputRingColor: "#1e3a5f",
    sendButtonBg: "#1e3a5f",
    sendButtonHover: "#2a4f7a",
    shortDescription: "Mental Models & Rational Thinking",
    // Round glasses
    iconPath:
      "M8 13a4 4 0 1 0 0-8 4 4 0 0 0 0 8Zm16 0a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM12 9h8M4 9H2m28 0h-2",
  },
  "benjamin-franklin": {
    id: "benjamin-franklin",
    primary: "#2d6a4f",
    secondary: "#95d5b2",
    gradientFrom: "#2d6a4f",
    gradientTo: "#95d5b2",
    bubbleBg: "rgba(45, 106, 79, 0.3)",
    bubbleText: "#d1fae5",
    headerBg: "rgba(45, 106, 79, 0.8)",
    headerText: "#95d5b2",
    cardGlow: "rgba(45, 106, 79, 0.4)",
    inputRingColor: "#2d6a4f",
    sendButtonBg: "#2d6a4f",
    sendButtonHover: "#3d8a6a",
    shortDescription: "Innovation & Self-Improvement",
    // Lightning bolt
    iconPath: "M18 2 L8 14 h6 L12 30 l10-14 h-6 Z",
  },
  "marcus-aurelius": {
    id: "marcus-aurelius",
    primary: "#6b21a8",
    secondary: "#a855f7",
    gradientFrom: "#6b21a8",
    gradientTo: "#a855f7",
    bubbleBg: "rgba(107, 33, 168, 0.3)",
    bubbleText: "#e9d5ff",
    headerBg: "rgba(107, 33, 168, 0.8)",
    headerText: "#a855f7",
    cardGlow: "rgba(107, 33, 168, 0.4)",
    inputRingColor: "#6b21a8",
    sendButtonBg: "#6b21a8",
    sendButtonHover: "#7c3aed",
    shortDescription: "Stoic Philosophy & Leadership",
    // Laurel wreath
    iconPath:
      "M16 4c-4 2-7 6-8 11 1-2 3-3 5-3m3-8c4 2 7 6 8 11-1-2-3-3-5-3M12 26c2-1 3-3 4-5m0 0c1 2 2 4 4 5",
  },
  "warren-buffett": {
    id: "warren-buffett",
    primary: "#166534",
    secondary: "#ca8a04",
    gradientFrom: "#166534",
    gradientTo: "#ca8a04",
    bubbleBg: "rgba(22, 101, 52, 0.3)",
    bubbleText: "#dcfce7",
    headerBg: "rgba(22, 101, 52, 0.8)",
    headerText: "#ca8a04",
    cardGlow: "rgba(22, 101, 52, 0.4)",
    inputRingColor: "#166534",
    sendButtonBg: "#166534",
    sendButtonHover: "#15803d",
    shortDescription: "Value Investing & Business Wisdom",
    // Rising chart line
    iconPath: "M4 24 L10 18 L16 20 L22 10 L28 6 M22 6 h6 v6",
  },
  confucius: {
    id: "confucius",
    primary: "#991b1b",
    secondary: "#ca8a04",
    gradientFrom: "#991b1b",
    gradientTo: "#ca8a04",
    bubbleBg: "rgba(153, 27, 27, 0.3)",
    bubbleText: "#fecaca",
    headerBg: "rgba(153, 27, 27, 0.8)",
    headerText: "#ca8a04",
    cardGlow: "rgba(153, 27, 27, 0.4)",
    inputRingColor: "#991b1b",
    sendButtonBg: "#991b1b",
    sendButtonHover: "#b91c1c",
    shortDescription: "Ethics & Harmonious Living",
    // Yin-yang / scroll
    iconPath:
      "M16 2a14 14 0 1 0 0 28A14 14 0 0 0 16 2Zm0 14a7 7 0 0 1 0-14 14 14 0 0 1 0 28 14 14 0 0 0 0-14Zm0-8a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm0 12a2 2 0 1 1 0 4 2 2 0 0 0 0-4Z",
  },
  "naval-ravikant": {
    id: "naval-ravikant",
    primary: "#0891b2",
    secondary: "#3b82f6",
    gradientFrom: "#0891b2",
    gradientTo: "#3b82f6",
    bubbleBg: "rgba(8, 145, 178, 0.3)",
    bubbleText: "#cffafe",
    headerBg: "rgba(8, 145, 178, 0.8)",
    headerText: "#3b82f6",
    cardGlow: "rgba(8, 145, 178, 0.4)",
    inputRingColor: "#0891b2",
    sendButtonBg: "#0891b2",
    sendButtonHover: "#06b6d4",
    shortDescription: "Wealth & Happiness Principles",
    // Network nodes
    iconPath:
      "M8 8m-3 0a3 3 0 1 0 6 0 3 3 0 1 0-6 0M24 8m-3 0a3 3 0 1 0 6 0 3 3 0 1 0-6 0M16 22m-3 0a3 3 0 1 0 6 0 3 3 0 1 0-6 0M10.5 10L14 19.5M21.5 10L18 19.5M11 8h10",
  },
};

// Default fallback theme
const defaultTheme: PersonaTheme = {
  id: "default",
  primary: "#6366f1",
  secondary: "#818cf8",
  gradientFrom: "#6366f1",
  gradientTo: "#818cf8",
  bubbleBg: "rgba(99, 102, 241, 0.3)",
  bubbleText: "#e0e7ff",
  headerBg: "rgba(99, 102, 241, 0.8)",
  headerText: "#818cf8",
  cardGlow: "rgba(99, 102, 241, 0.4)",
  inputRingColor: "#6366f1",
  sendButtonBg: "#6366f1",
  sendButtonHover: "#818cf8",
  shortDescription: "Wisdom & Knowledge",
  iconPath: "M16 4a12 12 0 1 0 0 24 12 12 0 0 0 0-24Zm0 6v6l4 4",
};

export function getPersonaTheme(personaId: string): PersonaTheme {
  return personaThemes[personaId] || defaultTheme;
}

export function getAllPersonaThemes(): Record<string, PersonaTheme> {
  return personaThemes;
}
