export type DocumentStatus = 'pending' | 'processing' | 'ready' | 'failed';

/* Guarda a origem física do arquivo para permitir reprocessamento posterior. */
export interface DocumentSource {
  originalName: string;
  storageKey: string;
  mimeType: string;
  sizeBytes: number;
}

export interface DocumentProperties {
  id: string;
  projectId: string;
  name: string;
  content: string;
  source?: DocumentSource;
  status: DocumentStatus;
  createdAt: Date;
}

const allowedStatusTransitions: Record<DocumentStatus, readonly DocumentStatus[]> = {
  pending: ['processing', 'failed'],
  processing: ['ready', 'failed'],
  ready: ['processing'],
  failed: ['processing'],
};

export class Document {
  private constructor(private readonly properties: DocumentProperties) {}

  static create(properties: Omit<DocumentProperties, 'status' | 'createdAt'>): Document {
    if (!properties.projectId.trim()) {
      throw new Error('Document projectId is required');
    }

    if (!properties.name.trim()) {
      throw new Error('Document name is required');
    }

    return new Document({
      ...properties,
      status: 'pending',
      createdAt: new Date(),
    });
  }

  changeStatus(nextStatus: DocumentStatus): void {
    if (nextStatus === this.properties.status) {
      return;
    }

    const allowedStatuses = allowedStatusTransitions[this.properties.status];
    if (!allowedStatuses.includes(nextStatus)) {
      throw new Error(
        `Invalid document status transition: ${this.properties.status} -> ${nextStatus}`,
      );
    }

    this.properties.status = nextStatus;
  }

  toJSON(): DocumentProperties {
    return { ...this.properties };
  }
}
