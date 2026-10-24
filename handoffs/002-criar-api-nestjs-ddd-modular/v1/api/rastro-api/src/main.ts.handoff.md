## Alteração: bootstrap HTTP

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/main.ts`
- Aplicação: `api`
- Localização: arquivo novo; função `bootstrap`
- Operação: `insert`
- Âncoras: arquivo inexistente.
- Motivo: configurar validação global, CORS controlado por ambiente e prefixo HTTP versionado.
- Impacto: endpoints ficam sob `/api/v1`; payloads desconhecidos são rejeitados.
- Pré-requisitos: `app.module.ts` e dependências do `package.json`.

### Código copiável

```typescript
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { ConfigService } from '@nestjs/config';
import { AppModule } from './app.module';

async function bootstrap(): Promise<void> {
  const app = await NestFactory.create(AppModule);
  const configService = app.get(ConfigService);

  app.setGlobalPrefix('api/v1');
  app.enableCors({
    origin: configService.get<string>('CORS_ORIGIN', '*'),
  });
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
    }),
  );

  await app.listen(configService.get<number>('PORT', 3000));
}

void bootstrap();
```

### Verificação

`GET /api/v1/health` deve retornar HTTP 200.
