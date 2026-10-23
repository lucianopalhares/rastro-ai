
import { Document } from '../domain/document';
import { DocumentRepository } from '../application/document.repository';

export class InMemoryDocumentRepository implements DocumentRepository {
  private readonly documents: Document[] = [];

  async save(document: Document): Promise<void> {
    this.documents.push(document);
  }

  async findAll(): Promise<Document[]> {
    return [...this.documents];
  }
}

