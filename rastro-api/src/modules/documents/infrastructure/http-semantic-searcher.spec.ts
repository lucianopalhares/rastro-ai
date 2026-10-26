import { HttpSemanticSearcher } from './http-semantic-searcher';

describe('HttpSemanticSearcher', () => {
  afterEach(() => {
    jest.restoreAllMocks();
  });

  /**
   * Confirma que a API envia consulta, projeto e limite ao Rastro AI.
   * Histórico: 023-v1 — cobre o contrato HTTP da busca semântica.
   */
  it('posts the search contract and returns results', async () => {
    const results = [
      {
        documentId: 'doc-1',
        chunkIndex: 0,
        content: 'Usar PostgreSQL.',
        startOffset: 0,
        endOffset: 17,
        projectId: 'project-1',
        score: 0.91,
        citation: {
          documentId: 'doc-1',
          chunkIndex: 0,
          startOffset: 0,
          endOffset: 17,
          excerpt: 'Usar PostgreSQL.',
        },
      },
    ];
    const fetchMock = jest
      .spyOn(global, 'fetch')
      .mockResolvedValue(
        new Response(
          JSON.stringify({ projectId: 'project-1', query: 'qual banco?', results }),
          { status: 200 },
        ),
      );

    await expect(new HttpSemanticSearcher().search('project-1', 'qual banco?', 3)).resolves.toEqual(
      expect.objectContaining({ projectId: 'project-1', query: 'qual banco?', results }),
    );
    expect(fetchMock).toHaveBeenCalledWith(
      'http://ai-indexer:8000/search',
      expect.objectContaining({
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ projectId: 'project-1', query: 'qual banco?', limit: 3 }),
      }),
    );
  });

  /**
   * Confirma que falhas do Rastro AI não viram resultados silenciosos.
   * Histórico: 023-v1 — protege o contrato de erro entre aplicações.
   */
  it('rejects when the Python search endpoint fails', async () => {
    jest.spyOn(global, 'fetch').mockResolvedValue(new Response(null, { status: 503 }));

    await expect(new HttpSemanticSearcher().search('project-1', 'qual banco?', 3)).rejects.toThrow(
      'Python semantic search failed with HTTP 503',
    );
  });
});
