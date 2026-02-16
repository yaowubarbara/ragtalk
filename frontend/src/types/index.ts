export interface Persona {
  id: string;
  name: string;
  title: string;
  avatar_url: string;
  description: string;
  greeting: string;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}
