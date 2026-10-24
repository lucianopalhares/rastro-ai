
export type DocumentStatus = 'pending' | 'processing' | 'ready' | 'failed';

/**
 * Identifica o arquivo físico associado ao documento.
 *
 * v1 = adicionou os metadados mínimos para reprocessamento do arquivo.
 */
export interface DocumentSource {
  originalName: string;
  storageKey: string;
  mimeType: string;
  sizeBytes: number;
}

/**
 * Reúne os dados persistidos e serializados de um documento.
 *
 * v1 = adicionou a origem opcional do arquivo sem quebrar criações JSON.
 */
export interface DocumentProperties {
  id: string;
  projectId: string;
  name: string;
  content: string;
  source?: DocumentSource;
  status: DocumentStatus;
  createdAt: Date;
}

const allowedStatusTransitions: Record<DocumentStatus, readonly DocumentStatus[]> = {
  pending: ['processing', 'failed'],
  processing: ['ready', 'failed'],
  ready: ['processing'],
  failed: ['processing'],
};

/**
 * Representa um documento pertencente a um projeto e seu ciclo de indexação.
 *
 * v1 = passou a aceitar a origem física opcional do arquivo enviado.
 */
export class Document {
  /**
   * Mantém as propriedades do agregado protegidas contra criação inválida.
   *
   * v1 = preservou a construção privada do documento.
   */
  private constructor(private readonly properties: DocumentProperties) {}

  /**
   * Cria um documento novo no estado pendente.
   *
   * v1 = preservou as validações e aceitou a origem opcional.
   */
  static create(properties: Omit<DocumentProperties, 'status' | 'createdAt'>): Document {
    if (!properties.projectId.trim()) {
      throw new Error('Document projectId is required');
    }

    if (!properties.name.trim()) {
      throw new Error('Document name is required');
    }

    return new Document({
      ...properties,
      status: 'pending',
      createdAt: new Date(),
    });
  }

  /**
   * Avança o documento somente por uma transição permitida.
   *
   * v1 = manteve as regras de ciclo de vida existentes.
   */
  changeStatus(nextStatus: DocumentStatus): void {
    if (nextStatus === this.properties.status) {
      return;
    }

    const allowedStatuses = allowedStatusTransitions[this.properties.status];
    if (!allowedStatuses.includes(nextStatus)) {
      throw new Error(
        `Invalid document status transition: ${this.properties.status} -> ${nextStatus}`,
      );
    }

    this.properties.status = nextStatus;
  }

  /**
   * Expõe uma cópia serializável das propriedades do documento.
   *
   * v1 = passou a incluir os metadados de origem quando presentes.
   */
  toJSON(): DocumentProperties {
    return { ...this.properties };
  }
}
