## Alteração: composição do módulo de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/documents.module.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `DocumentsModule`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: montar o bounded context e seus adapters por injeção de dependência.
- Impacto: mantém domínio, aplicação, infraestrutura e apresentação separados, permitindo trocar a persistência depois.
- Pré-requisitos: todos os arquivos do módulo de documentos.

### Código copiável

```typescript
import { Module } from '@nestjs/common';
import { CreateDocumentUseCase } from './application/create-document.use-case';
import { DocumentRepository } from './application/document.repository';
import { InMemoryDocumentRepository } from './infrastructure/in-memory-document.repository';
import { DocumentsController } from './presentation/documents.controller';

@Module({
  controllers: [DocumentsController],
  providers: [
    InMemoryDocumentRepository,
    {
      provide: 'DocumentRepository',
      useExisting: InMemoryDocumentRepository,
    },
    {
      provide: CreateDocumentUseCase,
      useFactory: (documentRepository: DocumentRepository) =>
        new CreateDocumentUseCase(documentRepository),
      inject: ['DocumentRepository'],
    },
  ],
})
export class DocumentsModule {}
```

### Verificação

Confirmar que a aplicação inicia sem erro de DI e que o controller recebe o mesmo repositório usado pelo caso de uso.
