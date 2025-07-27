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
}

export interface FileInfo {
  id: number;
  filename: string;
  content_type: string;
  file_size: number;
  word_count: number;
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

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  async uploadFile(
    file: File,
    metadata?: Record<string, unknown>
  ): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append("file", file);

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

  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error("Health check failed");
    }

    return response.json();
  }
}

export const apiService = new ApiService();
