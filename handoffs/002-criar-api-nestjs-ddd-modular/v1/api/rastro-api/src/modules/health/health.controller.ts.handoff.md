## Alteração: endpoint de saúde

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/health/health.controller.ts`
- Aplicação: `api`
- Localização: arquivo novo; classe `HealthController` e método `getHealth`
- Operação: `insert`
- Âncoras: diretório inexistente.
- Motivo: fornecer uma verificação determinística de processo e versão da API.
- Impacto: `GET /api/v1/health` não depende de banco ou serviço externo nesta etapa.
- Pré-requisitos: `HealthModule`.

### Código copiável

```typescript
import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  @Get()
  getHealth(): { status: string; service: string; timestamp: string } {
    return {
      status: 'ok',
      service: 'rastro-api',
      timestamp: new Date().toISOString(),
    };
  }
}
```

### Verificação

Com a aplicação em execução, `curl http://localhost:3000/api/v1/health` deve responder JSON com `status: "ok"`.
