## Alteração: módulo de saúde

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/health/health.module.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `HealthModule`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: isolar o endpoint operacional de saúde em um módulo próprio.
- Impacto: permite health check independente dos bounded contexts de negócio.
- Pré-requisitos: `health.controller.ts`.

### Código copiável

```typescript
import { Module } from '@nestjs/common';
import { HealthController } from './health.controller';

@Module({
  controllers: [HealthController],
})
export class HealthModule {}
```

### Verificação

O módulo deve ser importado pelo `AppModule` e expor somente o controller de health.
