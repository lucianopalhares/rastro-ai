import { DocumentProperties } from '../domain/document';
import { DocumentIndexer } from '../application/document-indexer';

/**
 * Encaminha documentos para o endpoint HTTP do indexador Python.
 * Existe para integrar processos separados sem acoplar o domínio à implementação Python.
 * Histórico: v1 — cria o cliente HTTP com timeout e validação de resposta.
 * v2 — publica o modelo serializado dentro do contrato `document`.
 */
export class HttpDocumentIndexer implements DocumentIndexer {
  private readonly endpoint = process.env.AI_INDEXING_URL ?? 'http://ai-indexer:8000/index';

  /**
   * Envia o documento e falha quando o serviço Python não confirma a indexação.
   * Histórico: v1 — implementa POST JSON com timeout configurável.
   */
  async index(input: DocumentProperties): Promise<void> {
    const controller = new AbortController();
    const timeout = setTimeout(
      () => controller.abort(),
      Number(process.env.AI_INDEXING_TIMEOUT_MS ?? 10000),
    );

    try {
      const response = await fetch(this.endpoint, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ document: input }),
        signal: controller.signal,
      });

      if (!response.ok) {
        throw new Error(`Python indexing failed with HTTP ${response.status}`);
      }
    } finally {
      clearTimeout(timeout);
    }
  }
}
