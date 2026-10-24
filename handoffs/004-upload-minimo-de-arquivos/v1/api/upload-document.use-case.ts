/* Coordena validação, persistência do arquivo e criação do documento pendente. */
import { randomUUID } from 'node:crypto';
import { Document } from '../domain/document';
import { DocumentRepository } from './document.repository';
import { DocumentFileStorage } from './document-file.storage';

export interface UploadDocumentInput {
  projectId: string;
  originalName: string;
  mimeType: string;
  sizeBytes: number;
  content: Buffer;
}

export class UploadDocumentUseCase {
  constructor(
    private readonly documentRepository: DocumentRepository,
    private readonly documentFileStorage: DocumentFileStorage,
  ) {}

  async execute(input: UploadDocumentInput): Promise<ReturnType<Document['toJSON']>> {
    const extension = this.getSupportedExtension(input.originalName);
    const content = input.content.toString('utf8');

    if (!content.trim()) {
      throw new Error('Document file content is required');
    }

    const documentId = randomUUID();
    const storageKey = await this.documentFileStorage.save({
      documentId,
      extension,
      content: input.content,
    });
    const document = Document.create({
      id: documentId,
      projectId: input.projectId,
      name: input.originalName,
      content,
      source: {
        originalName: input.originalName,
        storageKey,
        mimeType: input.mimeType,
        sizeBytes: input.sizeBytes,
      },
    });

    await this.documentRepository.save(document);
    return document.toJSON();
  }

  private getSupportedExtension(originalName: string): '.md' | '.txt' {
    const normalizedName = originalName.trim().toLowerCase();
    if (normalizedName.endsWith('.md')) {
      return '.md';
    }

    if (normalizedName.endsWith('.txt')) {
      return '.txt';
    }

    throw new Error('Only .md and .txt files are supported');
  }
}
