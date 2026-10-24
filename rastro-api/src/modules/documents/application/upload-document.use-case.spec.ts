import { Document } from '../domain/document';
import { DocumentFileStorage } from './document-file.storage';
import { DocumentRepository } from './document.repository';
import { UploadDocumentUseCase } from './upload-document.use-case';

/**
 * Verifica o upload sem depender do sistema de arquivos real.
 *
 * v1 = criou os cenários de associação, extensão inválida e conteúdo vazio.
 */
describe('UploadDocumentUseCase', () => {
  const savedDocuments: Document[] = [];
  const documentRepository: DocumentRepository = {
    /**
     * Guarda o documento em memória para a expectativa do teste.
     *
     * v1 = adicionou um repositório falso local ao cenário.
     */
    save: async (document) => {
      savedDocuments.push(document);
    },
    /**
     * Retorna os documentos salvos pelo cenário.
     *
     * v1 = completou o contrato do repositório falso.
     */
    findAll: async () => savedDocuments,
  };
  const storedFiles: Buffer[] = [];
  const documentFileStorage: DocumentFileStorage = {
    /**
     * Registra os bytes recebidos e devolve uma chave simulada.
     *
     * v1 = isolou o caso de uso do armazenamento local.
     */
    save: async ({ documentId, extension, content }) => {
      storedFiles.push(content);
      return `${documentId}${extension}`;
    },
  };

  /**
   * Limpa os dublês antes de cada cenário.
   *
   * v1 = evitou que um teste influencie o seguinte.
   */
  beforeEach(() => {
    savedDocuments.length = 0;
    storedFiles.length = 0;
  });

  /**
   * Confirma que arquivo suportado vira documento pendente associado.
   *
   * v1 = cobriu a persistência e os metadados de origem.
   */
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

  /**
   * Confirma que formatos não suportados e conteúdo vazio são rejeitados.
   *
   * v1 = cobriu as validações mínimas do upload.
   */
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
