import { create } from "zustand";
import { persist } from "zustand/middleware";
import { apiService } from "../services/api";

export interface ChatMessage {
  id: string;
  type: "user" | "assistant";
  content: string;
  timestamp: Date;
  sources?: string[];
  confidence?: number;
  anonymized_content?: string; // Debug: original AI response before deanonymization
}

interface ChatStore {
  // State
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;

  // Actions
  sendMessage: (question: string) => Promise<void>;
  clearMessages: () => void;
  addMessage: (message: ChatMessage) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      // Initial state
      messages: [],
      isLoading: false,
      error: null,

      // Actions
      sendMessage: async (question: string) => {
        if (!question.trim()) return;

        const { addMessage, setLoading, setError } = get();

        // Add user message
        const userMessage: ChatMessage = {
          id: Date.now().toString(),
          type: "user",
          content: question,
          timestamp: new Date(),
        };

        addMessage(userMessage);
        setLoading(true);
        setError(null);

        try {
          // Call the API
          const response = await apiService.askQuestion({
            question,
            context_limit: 5,
          });

          // Add assistant message
          const assistantMessage: ChatMessage = {
            id: (Date.now() + 1).toString(),
            type: "assistant",
            content: response.answer,
            timestamp: new Date(),
            sources: response.sources,
            confidence: response.confidence,
            anonymized_content: response.anonymized_answer,
          };

          addMessage(assistantMessage);
        } catch (err) {
          setError(err instanceof Error ? err.message : "Failed to get answer");
        } finally {
          setLoading(false);
        }
      },

      clearMessages: () => {
        set({ messages: [], error: null });
      },

      addMessage: (message: ChatMessage) => {
        set((state) => ({
          messages: [...state.messages, message],
        }));
      },

      setLoading: (loading: boolean) => {
        set({ isLoading: loading });
      },

      setError: (error: string | null) => {
        set({ error });
      },
    }),
    {
      name: "chat-storage", // unique name for localStorage key
      partialize: (state) => ({ messages: state.messages }), // only persist messages
    }
  )
);
