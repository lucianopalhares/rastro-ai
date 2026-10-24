## Alteração: caso de uso de criação

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/application/create-document.use-case.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `CreateDocumentUseCase` e método `execute`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: separar a regra de aplicação do controller e da infraestrutura.
- Impacto: criação de documento pode ser chamada por HTTP, fila ou outro adaptador.
- Pré-requisitos: `Document` e `DocumentRepository`.

### Código copiável

```typescript
import { randomUUID } from 'node:crypto';
import { Document } from '../domain/document';
import { DocumentRepository } from './document.repository';

export interface CreateDocumentInput {
  name: string;
  content: string;
}

export class CreateDocumentUseCase {
  constructor(private readonly documentRepository: DocumentRepository) {}

  async execute(input: CreateDocumentInput): Promise<ReturnType<Document['toJSON']>> {
    const document = Document.create({
      id: randomUUID(),
      name: input.name,
      content: input.content,
    });

    await this.documentRepository.save(document);
    return document.toJSON();
  }
}
```

### Verificação

O caso de uso deve persistir exatamente uma entidade e devolver sua representação serializável.
