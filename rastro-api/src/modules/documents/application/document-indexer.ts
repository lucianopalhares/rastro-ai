import { DocumentProperties } from '../domain/document';

/**
 * Define a porta usada para encaminhar o modelo de documento ao indexador Python.
 * Existe para manter o caso de uso de upload independente do transporte HTTP.
 * Histórico: v1 — cria o contrato da integração API → Python.
 * v2 — reutiliza as propriedades serializadas do domínio Document.
 */
export interface DocumentIndexer {
  /**
   * Solicita a extração, divisão e persistência vetorial de um documento.
   * Histórico: v1 — adiciona o payload mínimo com identidade, projeto e conteúdo.
   * v2 — recebe o modelo serializado já criado pelo caso de uso de upload.
   */
  index(input: DocumentProperties): Promise<void>;
}
