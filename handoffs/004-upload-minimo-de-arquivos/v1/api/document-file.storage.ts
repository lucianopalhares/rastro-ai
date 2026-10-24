/* Define o contrato mínimo para trocar o armazenamento local por object storage depois. */
export interface SaveDocumentFileInput {
  documentId: string;
  extension: '.md' | '.txt';
  content: Buffer;
}

/**
 * descricao do metodo de interface e porque
 *
 * v1 = mudou a variavel para string
 * v2 = adicionou dois pontos
 */
export interface DocumentFileStorage {
  save(input: SaveDocumentFileInput): Promise<string>;
}
