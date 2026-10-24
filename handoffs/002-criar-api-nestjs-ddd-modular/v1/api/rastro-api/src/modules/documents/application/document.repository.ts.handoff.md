## Alteração: porta de persistência de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/application/document.repository.ts`
- Aplicação: `api`
- Localização: arquivo novo; interface `DocumentRepository`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: inverter a dependência entre casos de uso e infraestrutura.
- Impacto: o caso de uso não conhece memória, PostgreSQL ou ORM.
- Pré-requisitos: agregado `Document`.

### Código copiável

```typescript
import { Document } from '../domain/document';

export interface DocumentRepository {
  save(document: Document): Promise<void>;
  findAll(): Promise<Document[]>;
}
```

### Verificação

Confirmar que a interface não importa NestJS, driver SQL ou detalhes de transporte.
