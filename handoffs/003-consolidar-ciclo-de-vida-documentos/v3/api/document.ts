## Alteração: completar o agregado Document após aplicação parcial

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/domain/document.ts`
- Aplicação: `api`
- Localização: linhas 2–30, tipo `DocumentStatus`, interface `DocumentProperties` e classe `Document`.
- Operação: replace
- Âncoras: substituir do `export type DocumentStatus` até o fechamento da classe `Document`.
- O que o trecho faz: adiciona `projectId`, estados de indexação e transições válidas.
- Motivo: o caso de uso já envia `projectId`, mas o agregado real ainda não aceita esse campo.
- Impacto: elimina o erro `TS2353` e formaliza o ciclo de vida documental.
- Dependências: nenhuma; aplicar antes da validação final do controller.

### Conteúdo atual

```ts
export type DocumentStatus = 'pending' | 'ready';

export interface DocumentProperties {
  id: string;
  name: string;
  content: string;
  status: DocumentStatus;
  createdAt: Date;
}

export class Document {
  private constructor(private readonly properties: DocumentProperties) {}

  static create(properties: Omit<DocumentProperties, 'status' | 'createdAt'>): Document {
    if (!properties.name.trim()) {
      throw new Error('Document name is required');
    }

    return new Document({
      ...properties,
      status: 'pending',
      createdAt: new Date(),
    });
  }

  toJSON(): DocumentProperties {
    return { ...this.properties };
  }
}
```

### Conteúdo copiável

```ts
export type DocumentStatus = 'pending' | 'processing' | 'ready' | 'failed';

export interface DocumentProperties {
  id: string;
  projectId: string;
  name: string;
  content: string;
  status: DocumentStatus;
  createdAt: Date;
}

const allowedStatusTransitions: Record<DocumentStatus, readonly DocumentStatus[]> = {
  pending: ['processing', 'failed'],
  processing: ['ready', 'failed'],
  ready: ['processing'],
  failed: ['processing'],
};

export class Document {
  private constructor(private readonly properties: DocumentProperties) {}

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

  toJSON(): DocumentProperties {
    return { ...this.properties };
  }
}
```

### Explicação do trecho

- O código faz: torna compatível o agregado com o `projectId` já aplicado no caso de uso e controla estados válidos.
- Por que substituir: manter o domínio antigo causa o erro `TS2353` durante a compilação.
- O que permanece inalterado: persistência em memória, criação com `pending` e conteúdo textual.

### Verificação

1. Aplicar a substituição no arquivo original.
2. Executar `npm run build` em `/home/dev/dev/ia/rastro-ai/rastro-api`.
3. Confirmar que o erro sobre `projectId` desapareceu.
