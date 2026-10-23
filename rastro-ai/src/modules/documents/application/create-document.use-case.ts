
import { randomUUID } from 'node:crypto';
import { Document } from '../domain/document';
import { DocumentRepository } from './document.repository';

export interface CreateDocumentInput {
  name: string;
  content: string;
}

export class CreateDocumentUseCase {
  constructor(private readonly documentRepository: DocumentRepository) {}

  async execute(input: CreateDocumentInput): Promise<ReturnType<Document['toJSON']>> {
    const document = Document.create({
      id: randomUUID(),
      name: input.name,
      content: input.content,
    });

    await this.documentRepository.save(document);
    return document.toJSON();
  }
}

