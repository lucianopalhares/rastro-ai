import { randomUUID } from 'node:crypto';
import { Document } from '../domain/document';
import { DocumentFileStorage } from './document-file.storage';
import { DocumentRepository } from './document.repository';

/**
 * Define os dados recebidos no upload mínimo de um documento.
 *
 * v1 = criou o contrato para projeto, arquivo, conteúdo e metadados HTTP.
 */
export interface UploadDocumentInput {
  projectId: string;
  originalName: string;
  mimeType: string;
  sizeBytes: number;
  content: Buffer;
}

/**
 * Valida, armazena e associa um arquivo a um documento pendente.
 *
 * v1 = criou o fluxo síncrono mínimo antes da futura indexação assíncrona.
 */
export class UploadDocumentUseCase {
  constructor(
    private readonly documentRepository: DocumentRepository,
    private readonly documentFileStorage: DocumentFileStorage,
  ) {}

  /**
   * Grava os bytes, cria o documento e retorna seus dados serializáveis.
   *
   * v1 = aceitou somente arquivos não vazios com extensão `.md` ou `.txt`.
   */
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

  /**
   * Retorna a extensão permitida ou interrompe o upload inválido.
   *
   * v1 = restringiu o MVP aos formatos `.md` e `.txt`.
   */
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
