/* Verifica o contrato de upload sem depender do sistema de arquivos real. */
import { Document } from '../domain/document';
import { DocumentRepository } from './document.repository';
import { DocumentFileStorage } from './document-file.storage';
import { UploadDocumentUseCase } from './upload-document.use-case';

describe('UploadDocumentUseCase', () => {
  const savedDocuments: Document[] = [];
  const documentRepository: DocumentRepository = {
    save: async (document) => {
      savedDocuments.push(document);
    },
    findAll: async () => savedDocuments,
  };
  const storedFiles: Buffer[] = [];
  const documentFileStorage: DocumentFileStorage = {
    save: async ({ documentId, extension, content }) => {
      storedFiles.push(content);
      return `${documentId}${extension}`;
    },
  };

  beforeEach(() => {
    savedDocuments.length = 0;
    storedFiles.length = 0;
  });

  it('stores a supported file and associates it with the document', async () => {
    const useCase = new UploadDocumentUseCase(documentRepository, documentFileStorage);

    const document = await useCase.execute({
      projectId: 'project-1',
      originalName: 'meeting.md',
      mimeType: 'text/markdown',
      sizeBytes: 22,
      content: Buffer.from('# Decision\nUse PostgreSQL.', 'utf8'),
    });

    expect(document.status).toBe('pending');
    expect(document.source).toMatchObject({
      originalName: 'meeting.md',
      mimeType: 'text/markdown',
    });
    expect(document.source?.storageKey).toMatch(/\.md$/);
    expect(storedFiles).toHaveLength(1);
  });

  it('rejects unsupported extensions and empty content', async () => {
    const useCase = new UploadDocumentUseCase(documentRepository, documentFileStorage);

    await expect(
      useCase.execute({
        projectId: 'project-1',
        originalName: 'meeting.pdf',
        mimeType: 'application/pdf',
        sizeBytes: 1,
        content: Buffer.from('content'),
      }),
    ).rejects.toThrow('Only .md and .txt files are supported');

    await expect(
      useCase.execute({
        projectId: 'project-1',
        originalName: 'empty.txt',
        mimeType: 'text/plain',
        sizeBytes: 1,
        content: Buffer.from('  '),
      }),
    ).rejects.toThrow('Document file content is required');
  });
});
