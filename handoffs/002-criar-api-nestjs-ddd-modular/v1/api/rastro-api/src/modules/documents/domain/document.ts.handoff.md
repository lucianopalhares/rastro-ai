## Alteração: agregado de documento

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/domain/document.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `Document`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: concentrar identidade e invariantes básicas do documento no domínio, sem depender do NestJS ou de persistência.
- Impacto: o domínio permanece independente de HTTP e banco.
- Pré-requisitos: nenhum.

### Código copiável

```typescript
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

### Verificação

Testar que nome vazio lança erro e que um documento criado inicia com status `pending`.
