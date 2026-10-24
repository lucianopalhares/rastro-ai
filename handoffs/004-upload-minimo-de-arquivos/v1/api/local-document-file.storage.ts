/* Persiste os bytes fora do banco usando uma chave segura gerada pelo caso de uso. */
import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import {
  DocumentFileStorage,
  SaveDocumentFileInput,
} from '../application/document-file.storage';

export class LocalDocumentFileStorage implements DocumentFileStorage {
  private readonly rootDirectory = resolve(
    process.env.DOCUMENT_STORAGE_PATH ?? join(process.cwd(), 'storage', 'documents'),
  );

  async save(input: SaveDocumentFileInput): Promise<string> {
    const storageKey = `${input.documentId}${input.extension}`;
    const filePath = join(this.rootDirectory, storageKey);

    await mkdir(dirname(filePath), { recursive: true });
    await writeFile(filePath, input.content, { flag: 'wx' });

    return storageKey;
  }
}
