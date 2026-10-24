## Alteração: adaptador de memória

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/infrastructure/in-memory-document.repository.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `InMemoryDocumentRepository`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: permitir execução local da primeira API sem antecipar o adapter PostgreSQL.
- Impacto: os dados são perdidos ao reiniciar; a interface permite substituição posterior sem alterar o caso de uso.
- Pré-requisitos: `Document` e `DocumentRepository`.

### Código copiável

```typescript
import { Document } from '../domain/document';
import { DocumentRepository } from '../application/document.repository';

export class InMemoryDocumentRepository implements DocumentRepository {
  private readonly documents: Document[] = [];

  async save(document: Document): Promise<void> {
    this.documents.push(document);
  }

  async findAll(): Promise<Document[]> {
    return [...this.documents];
  }
}
```

### Verificação

Criar dois documentos e confirmar que `findAll` retorna ambos sem expor o array interno.
