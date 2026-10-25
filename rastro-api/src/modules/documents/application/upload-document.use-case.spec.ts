import { Document } from '../domain/document';
import { DocumentFileStorage } from './document-file.storage';
import { DocumentIndexer } from './document-indexer';
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
  const indexedDocuments: string[] = [];
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

  const documentIndexer: DocumentIndexer = {
    /**
     * Registra a identidade indexada pelo dublê do serviço Python.
     * Histórico: v2 — cobre o contrato enviado após o armazenamento.
     */
    index: async (document) => {
      indexedDocuments.push(document.id);
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
    indexedDocuments.length = 0;
  });

  /**
   * Confirma que arquivo suportado vira documento pendente associado.
   *
   * v1 = cobriu a persistência e os metadados de origem.
   */
  it('stores a supported file and associates it with the document', async () => {
    const useCase = new UploadDocumentUseCase(
      documentRepository,
      documentFileStorage,
      documentIndexer,
    );

    const document = await useCase.execute({
      projectId: 'project-1',
      originalName: 'meeting.md',
      mimeType: 'text/markdown',
      sizeBytes: 22,
      content: Buffer.from('# Decision\nUse PostgreSQL.', 'utf8'),
    });

    expect(document.status).toBe('ready');
    expect(document.source).toMatchObject({
      originalName: 'meeting.md',
      mimeType: 'text/markdown',
    });
    expect(document.source?.storageKey).toMatch(/\.md$/);
    expect(storedFiles).toHaveLength(1);
    expect(indexedDocuments).toHaveLength(1);
  });

  /**
   * Confirma que formatos não suportados e conteúdo vazio são rejeitados.
   *
   * v1 = cobriu as validações mínimas do upload.
   */
  it('rejects unsupported extensions and empty content', async () => {
    const useCase = new UploadDocumentUseCase(
      documentRepository,
      documentFileStorage,
      documentIndexer,
    );

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

  /**
   * Confirma que uma falha Python fica registrada sem perder o documento salvo.
   * Histórico: v2 — cobre a transição para `failed` no fluxo integrado.
   */
  it('stores a failed status when indexing is unavailable', async () => {
    const failingIndexer: DocumentIndexer = {
      /**
       * Simula a indisponibilidade do serviço Python.
       * Histórico: v2 — cria o cenário de falha de integração.
       */
      index: async () => {
        throw new Error('Python unavailable');
      },
    };
    const useCase = new UploadDocumentUseCase(
      documentRepository,
      documentFileStorage,
      failingIndexer,
    );

    const document = await useCase.execute({
      projectId: 'project-1',
      originalName: 'meeting.txt',
      mimeType: 'text/plain',
      sizeBytes: 7,
      content: Buffer.from('content'),
    });

    expect(document.status).toBe('failed');
  });
});
