import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import {
  DocumentFileStorage,
  SaveDocumentFileInput,
} from '../application/document-file.storage';

/**
 * Armazena arquivos em uma pasta local configurável do serviço.
 *
 * v1 = criou o adaptador local com chave baseada no identificador do documento.
 */
export class LocalDocumentFileStorage implements DocumentFileStorage {
  private readonly rootDirectory = resolve(
    process.env.DOCUMENT_STORAGE_PATH ?? join(process.cwd(), 'storage', 'documents'),
  );

  /**
   * Cria a pasta e grava o arquivo sem sobrescrever outro.
   *
   * v1 = adicionou persistência local com escrita exclusiva.
   */
  async save(input: SaveDocumentFileInput): Promise<string> {
    const storageKey = `${input.documentId}${input.extension}`;
    const filePath = join(this.rootDirectory, storageKey);

    await mkdir(dirname(filePath), { recursive: true });
    await writeFile(filePath, input.content, { flag: 'wx' });

    return storageKey;
  }
}
