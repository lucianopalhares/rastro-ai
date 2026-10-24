## Alteração: controller HTTP de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/modules/documents/presentation/documents.controller.ts`
- Aplicação: `api`
- Localização: arquivo ausente no diretório `src/modules/documents/presentation/`, importado por `DocumentsModule`.
- Operação: `insert`
- Âncoras: arquivo inexistente; criar após o diretório `presentation/` e antes da compilação do módulo.
- O que o trecho faz: adapta requisições HTTP aos casos de uso e ao repositório de documentos.
- Motivo: `documents.module.ts` importa `./presentation/documents.controller`, mas o arquivo correspondente não existe no código real.
- Impacto: elimina `TS2307` e adiciona `POST /api/v1/documents` e `GET /api/v1/documents`.
- Pré-requisitos: `CreateDocumentUseCase`, `DocumentRepository` e `ValidationPipe` já presentes na API.

### Localização exata

```text
Trecho anterior:
import { DocumentsController } from './presentation/documents.controller';

Ponto estrutural:
novo arquivo src/modules/documents/presentation/documents.controller.ts

Trecho posterior:
@Module({
  controllers: [DocumentsController],
```

### Conteúdo copiável

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

### Explicação do trecho

- O que este código faz: valida o formato básico do payload, cria documentos pelo caso de uso e lista documentos pelo contrato do repositório.
- Por que inserir: o módulo já depende dessa classe e o compilador não encontra o arquivo importado.
- O que permanece inalterado: domínio, caso de uso, persistência em memória e composição do módulo.

### Aplicação e verificação

1. Criar o diretório `rastro-ai/src/modules/documents/presentation/` se necessário.
2. Criar o arquivo indicado com o conteúdo copiável.
3. Executar `docker compose exec api npm run build`.
4. Com a API em execução, testar `POST /api/v1/documents` com `{"name":"meeting.md","content":"Decision"}`.
5. Testar `GET /api/v1/documents` e confirmar que o documento criado é listado.
