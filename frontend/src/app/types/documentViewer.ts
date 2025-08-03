export interface DocumentViewerProps {
  fileId: number;
  filename: string;
  contentType: string;
  onClose: () => void;
}

export interface DocumentViewerState {
  content: string | null;
  blobUrl: string | null;
  loading: boolean;
  error: string | null;
} 