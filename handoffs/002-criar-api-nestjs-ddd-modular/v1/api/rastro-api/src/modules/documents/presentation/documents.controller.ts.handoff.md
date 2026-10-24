## Alteração: controller HTTP de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/presentation/documents.controller.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `DocumentsController`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: adaptar HTTP aos casos de uso sem colocar regras de domínio no controller.
- Impacto: adiciona `POST /api/v1/documents` e `GET /api/v1/documents`.
- Pré-requisitos: `CreateDocumentUseCase` e `DocumentRepository` registrados pelo módulo.

### Código copiável

```typescript
import { Body, Controller, Get, Inject, Post } from '@nestjs/common';
import { IsNotEmpty, IsString } from 'class-validator';
import { CreateDocumentUseCase } from '../application/create-document.use-case';
import { DocumentRepository } from '../application/document.repository';

class CreateDocumentRequest {
  @IsString()
  @IsNotEmpty()
  name!: string;

  @IsString()
  @IsNotEmpty()
  content!: string;
}

@Controller('documents')
export class DocumentsController {
  constructor(
    private readonly createDocumentUseCase: CreateDocumentUseCase,
    @Inject('DocumentRepository')
    private readonly documentRepository: DocumentRepository,
  ) {}

  @Post()
  create(@Body() request: CreateDocumentRequest) {
    return this.createDocumentUseCase.execute(request);
  }

  @Get()
  async findAll() {
    const documents = await this.documentRepository.findAll();
    return documents.map((document) => document.toJSON());
  }
}
```

### Verificação

`POST /api/v1/documents` com `{"name":"meeting.md","content":"Decision"}` deve retornar HTTP 201; `GET` deve listar o documento.
