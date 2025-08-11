import { FileInfo, StatsResponse } from "../services/api";

export interface FileGridState {
  files: FileInfo[];
  loading: boolean;
  error: string | null;
}

export interface FileListState {
  stats: StatsResponse | null;
  loading: boolean;
  error: string | null;
}

export interface UploadState {
  isUploading: boolean;
  progress: number;
  error: string | null;
  success: string | null;
}

export interface FileContextType {
  refreshTrigger: number;
  triggerRefresh: () => void;
}
