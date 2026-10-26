import {
  SemanticSearchResponse,
  SemanticSearcher,
} from '../application/semantic-searcher';

/**
 * Encaminha consultas semânticas ao endpoint HTTP do Rastro AI.
 * Existe para preservar o PGVector e a geração de embeddings no serviço Python.
 * Histórico: 023-v1 — adiciona proxy com timeout e validação mínima da resposta.
 */
export class HttpSemanticSearcher implements SemanticSearcher {
  private readonly endpoint = process.env.AI_SEARCH_URL ?? 'http://ai-indexer:8000/search';

  /**
   * Busca chunks do projeto e preserva score e citação retornados pelo serviço de IA.
   * Histórico: 023-v1 — implementa POST JSON com limite configurável de espera.
   */
  async search(projectId: string, query: string, limit: number): Promise<SemanticSearchResponse> {
    const controller = new AbortController();
    const timeout = setTimeout(
      () => controller.abort(),
      Number(process.env.AI_SEARCH_TIMEOUT_MS ?? process.env.AI_INDEXING_TIMEOUT_MS ?? 60000),
    );

    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ projectId, query, limit }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Python semantic search failed with HTTP ${response.status}`);
      }

      const payload = (await response.json()) as Partial<SemanticSearchResponse>;
      if (
        payload.projectId !== projectId ||
        payload.query !== query ||
        !Array.isArray(payload.results)
      ) {
        throw new Error('Python semantic search returned an invalid result set');
      }
      return payload as SemanticSearchResponse;
    } finally {
      clearTimeout(timeout);
    }
  }
}
