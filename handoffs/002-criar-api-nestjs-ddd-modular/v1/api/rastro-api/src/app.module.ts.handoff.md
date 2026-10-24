## Alteração: módulo raiz

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/app.module.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `AppModule`
- Operação: `insert`
- Âncoras: arquivo inexistente.
- Motivo: registrar configuração e os módulos independentes da API.
- Impacto: a aplicação inicia com `HealthModule` e `DocumentsModule`, sem acoplá-los entre si.
- Pré-requisitos: módulos de health e documents.

### Código copiável

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { DocumentsModule } from './modules/documents/documents.module';
import { HealthModule } from './modules/health/health.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    HealthModule,
    DocumentsModule,
  ],
})
export class AppModule {}
```

### Verificação

O bootstrap deve resolver `ConfigService`, `HealthModule` e `DocumentsModule` sem erro de dependência circular.
