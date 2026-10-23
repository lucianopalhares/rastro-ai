
export type DocumentStatus = 'pending' | 'ready';

export interface DocumentProperties {
  id: string;
  name: string;
  content: string;
  status: DocumentStatus;
  createdAt: Date;
}

export class Document {
  private constructor(private readonly properties: DocumentProperties) {}

  static create(properties: Omit<DocumentProperties, 'status' | 'createdAt'>): Document {
    if (!properties.name.trim()) {
      throw new Error('Document name is required');
    }

    return new Document({
      ...properties,
      status: 'pending',
      createdAt: new Date(),
    });
  }

  toJSON(): DocumentProperties {
    return { ...this.properties };
  }
}

