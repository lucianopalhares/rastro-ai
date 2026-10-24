## Alteração: composição Docker de desenvolvimento da API

- Arquivo original: `/home/dev/dev/ia/rastro-ai/docker-compose.yml`
- Aplicação: `api`
- Operação: `replace`
- Âncoras: substituir o conteúdo atual do arquivo Compose.
- Motivo: selecionar explicitamente `Dockerfile.dev`, com `npm install`, bind mount e hot reload.
- Impacto: o fluxo local não depende de lockfile; `node_modules` permanece no volume do container.
- Dependências: `/home/dev/dev/ia/rastro-ai/rastro-ai/Dockerfile.dev`.

### Código copiável

```yaml
services:
  api:
    build:
      context: ./rastro-ai
      dockerfile: Dockerfile.dev
    command: npm run start:dev
    environment:
      NODE_ENV: development
      PORT: 3000
      CORS_ORIGIN: '*'
      CHOKIDAR_USEPOLLING: 'true'
    ports:
      - '3039:3000'
    volumes:
      - ./rastro-ai:/app
      - /app/node_modules
    healthcheck:
      test:
        - CMD-SHELL
        - >-
          node -e "fetch('http://127.0.0.1:3000/api/v1/health').then((response) =>
          process.exit(response.ok ? 0 : 1)).catch(() => process.exit(1))"
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 10s
```

### Verificação

Executar `docker compose config`, `docker compose build api` e `docker compose up -d`. O container deve ficar saudável em `127.0.0.1:3000`, e o host deve acessar `http://localhost:3039/api/v1/health`.
