## Alteração: ciclo de vida e escopo do agregado Document

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/modules/documents/domain/document.ts`
- Aplicação: `api`
- Localização: linhas 2–30, tipo `DocumentStatus`, interface `DocumentProperties` e classe `Document`.
- Operação: `replace`
- Âncoras: `export type DocumentStatus` até o fechamento da classe `Document`, entre o início do arquivo e o próximo arquivo do módulo.
- O que o trecho faz: adiciona o projeto proprietário, estados intermediários da indexação e transições válidas do agregado.
- Motivo: o fluxo da Fase 1 precisa distinguir documentos pendentes, em processamento, prontos e falhos antes da indexação.
- Impacto: documentos passam a exigir `projectId`; alterações de estado inválidas geram erro de domínio.
- Dependências: nenhuma dentro da tarefa; aplicar antes do caso de uso e do controller.

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

- O código faz: vincula cada documento a um projeto e controla as transições necessárias para a futura indexação.
- Por que substituir: o contrato atual não representa `processing` ou `failed` e não permite separar documentos por projeto.
- O que permanece inalterado: o documento continua sendo criado com status `pending`, o conteúdo permanece armazenado em memória e a persistência não é introduzida nesta tarefa.

### Verificação

1. Aplicar a substituição no arquivo original.
2. Executar `npm run build` dentro de `/home/dev/dev/ia/rastro-ai/rastro-ai`.
3. Confirmar nos testes que transições válidas funcionam e transições inválidas lançam erro.
