## Alteração: composição Docker de produção da API

- Arquivo original: `/home/dev/dev/ia/rastro-ai/docker-compose.production.yml`
- Aplicação: `api`
- Operação: `insert`
- Âncoras: arquivo inexistente; criar na raiz do projeto.
- Motivo: executar a imagem multi-stage de produção sem bind mount do código.
- Impacto: usa `Dockerfile`, exige `package-lock.json` e executa somente o bundle compilado.
- Dependências: `/home/dev/dev/ia/rastro-ai/rastro-ai/Dockerfile` e `rastro-ai/package-lock.json` versionado.

### Código copiável

```yaml
services:
  api:
    build:
      context: ./rastro-ai
      dockerfile: Dockerfile
    environment:
      NODE_ENV: production
      PORT: 3000
      CORS_ORIGIN: '*'
    ports:
      - '3039:3000'
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

Após gerar e versionar o lockfile, executar `docker compose -f docker-compose.production.yml config`, `docker compose -f docker-compose.production.yml build` e validar o endpoint publicado em `http://localhost:3039/api/v1/health`.
