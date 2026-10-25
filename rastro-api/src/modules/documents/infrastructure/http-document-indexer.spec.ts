import { HttpDocumentIndexer } from './http-document-indexer';
import { DocumentProperties } from '../domain/document';

describe('HttpDocumentIndexer', () => {
  const document: DocumentProperties = {
    id: 'doc-1',
    projectId: 'project-1',
    name: 'meeting.md',
    content: '# Decision',
    status: 'processing',
    createdAt: new Date('2026-10-24T00:00:00.000Z'),
  };
  /**
   * Restaura o boundary HTTP global após cada cenário.
   * Histórico: v1 — isola o cliente do serviço externo durante os testes.
   */
  afterEach(() => {
    jest.restoreAllMocks();
  });

  /**
   * Confirma o contrato JSON enviado ao endpoint Python.
   * Histórico: v1 — cobre o encaminhamento de identidade, projeto e conteúdo.
   */
  it('posts the document payload to the Python indexer', async () => {
    const fetchMock = jest.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ documentId: 'doc-1', chunks: 1 }), { status: 200 }),
    );
    const indexer = new HttpDocumentIndexer();

    await indexer.index(document);

    expect(fetchMock).toHaveBeenCalledWith(
      'http://ai-indexer:8000/index',
      expect.objectContaining({
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ document }),
      }),
    );
  });

  /**
   * Confirma que respostas HTTP não bem-sucedidas interrompem o fluxo.
   * Histórico: v1 — cobre a propagação de falha para o caso de uso do upload.
   */
  it('rejects when the Python indexer returns an error', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 503 }));

    await expect(
      new HttpDocumentIndexer().index(document),
    ).rejects.toThrow('Python indexing failed with HTTP 503');
  });
});
