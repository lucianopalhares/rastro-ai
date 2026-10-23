
import { Document } from '../domain/document';

export interface DocumentRepository {
  save(document: Document): Promise<void>;
  findAll(): Promise<Document[]>;
}
