/**
 * Define o contrato da busca semântica consumida pelo controller.
 * Existe para manter a API independente do transporte usado pelo Rastro AI.
 * Histórico: 023-v1 — cria o contrato público de resultados, scores e citações.
 */
export interface SemanticSearchResult {
  documentId: string;
  chunkIndex: number;
  content: string;
  startOffset: number;
  endOffset: number;
  projectId: string;
  score: number;
  citation: {
    documentId: string;
    chunkIndex: number;
    startOffset: number;
    endOffset: number;
    excerpt: string;
  };
}

/**
 * Representa a resposta completa da busca semântica, incluindo o escopo consultado.
 * Histórico: 023-v1 — evita que consumidores percam projeto e consulta ao ler resultados.
 */
export interface SemanticSearchResponse {
  projectId: string;
  query: string;
  results: SemanticSearchResult[];
}

/**
 * Abstrai a chamada da API para o endpoint de busca do serviço Python.
 * Histórico: 023-v1 — formaliza o contrato de consulta por projeto.
 */
export interface SemanticSearcher {
  search(projectId: string, query: string, limit: number): Promise<SemanticSearchResponse>;
}
