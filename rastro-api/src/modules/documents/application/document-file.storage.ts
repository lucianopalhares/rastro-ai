/**
 * Define como os bytes de um arquivo de documento são persistidos.
 *
 * v1 = criou o contrato para desacoplar o caso de uso do armazenamento local.
 */
export interface DocumentFileStorage {
  /**
   * Persiste o conteúdo e retorna a chave usada para localizá-lo.
   *
   * v1 = adicionou a operação mínima de armazenamento por documento.
   */
  save(input: SaveDocumentFileInput): Promise<string>;
}

/**
 * Reúne os dados necessários para gravar um arquivo de documento.
 *
 * v1 = criou o contrato com identificador, extensão e bytes do arquivo.
 */
export interface SaveDocumentFileInput {
  documentId: string;
  extension: '.md' | '.txt';
  content: Buffer;
}
