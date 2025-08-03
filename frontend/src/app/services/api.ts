// In development, use localhost:8000, in production you'd set NEXT_PUBLIC_API_URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface IngestResponse {
  message: string;
  filename: string;
  file_size: number;
  file_type: string;
  status: string;
  chunks_processed: number;
  word_count: number;
  anonymized: boolean;
  anonymization_summary?: Record<string, number>;
}

export interface FileInfo {
  id: number;
  filename: string;
  content_type: string;
  file_size: number;
  word_count: number;
  anonymized: boolean;
  created_at: string;
}

export interface StatsResponse {
  file_count: number;
  chunk_count: number;
  total_words: number;
}

export interface FilesResponse {
  files: FileInfo[];
}

export interface HealthResponse {
  status: string;
  message: string;
}

export interface QuestionRequest {
  question: string;
  context_limit: number;
}

export interface QuestionResponse {
  answer: string;
  sources: string[];
  confidence: number;
  anonymized_answer?: string; // Debug: original AI response before deanonymization
}

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async uploadFile(
    file: File,
    metadata?: Record<string, unknown>,
    anonymize: boolean = false
  ): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("anonymize", anonymize.toString());

    if (metadata) {
      formData.append("metadata", JSON.stringify(metadata));
    }

    const response = await fetch(`${this.baseUrl}/ingest`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Upload failed" }));
      throw new Error(errorData.detail || "Upload failed");
    }

    return response.json();
  }

  async getStats(): Promise<StatsResponse> {
    const response = await fetch(`${this.baseUrl}/stats`);

    if (!response.ok) {
      throw new Error("Failed to fetch stats");
    }

    return response.json();
  }

  async getFiles(): Promise<FilesResponse> {
    const response = await fetch(`${this.baseUrl}/files`);

    if (!response.ok) {
      throw new Error("Failed to fetch files");
    }

    return response.json();
  }

  async getFileContent(fileId: number): Promise<{ content: string }> {
    const response = await fetch(`${this.baseUrl}/files/${fileId}/content`);

    if (!response.ok) {
      throw new Error("Failed to fetch file content");
    }

    return response.json();
  }

  async getFileBlob(fileId: number): Promise<Blob> {
    const response = await fetch(`${this.baseUrl}/files/${fileId}/download`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(
        `Failed to fetch file ${fileId}:`,
        response.status,
        errorText
      );
      throw new Error(`Failed to fetch file: ${response.status} ${errorText}`);
    }

    const blob = await response.blob();
    if (blob.size === 0) {
      console.error(`File ${fileId} returned empty blob`);
      throw new Error("File is empty");
    }

    console.log(
      `Successfully fetched file ${fileId}, size: ${blob.size} bytes`
    );
    return blob;
  }

  async deleteFile(fileId: number): Promise<{ message: string }> {
    const response = await fetch(`${this.baseUrl}/files/${fileId}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Failed to delete file" }));
      throw new Error(errorData.detail || "Failed to delete file");
    }

    return response.json();
  }

  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error("Health check failed");
    }

    return response.json();
  }

  async askQuestion(request: QuestionRequest): Promise<QuestionResponse> {
    const response = await fetch(`${this.baseUrl}/ask`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ detail: "Failed to ask question" }));
      throw new Error(errorData.detail || "Failed to ask question");
    }

    return response.json();
  }
}

export const apiService = new ApiService();
