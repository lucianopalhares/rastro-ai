## Alteração: imagem de desenvolvimento da API

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-ai/Dockerfile.dev`
- Aplicação: `api`
- Operação: `insert`
- Âncoras: arquivo inexistente; criar na raiz da aplicação.
- Motivo: permitir `npm install` no container de desenvolvimento, sem acoplar o fluxo local ao lockfile de produção.
- Impacto: mantém dependências de desenvolvimento e funciona com bind mount e hot reload.
- Dependências: `package.json`, `tsconfig*.json`, `nest-cli.json` e `src/`.

### Código copiável

```dockerfile
FROM node:22-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY tsconfig*.json nest-cli.json ./
COPY src ./src
EXPOSE 3000
CMD ["npm", "run", "start:dev"]
```

### Verificação

`docker compose build api` usando `docker-compose.yml` deve concluir sem `package-lock.json`; `docker compose up -d` deve iniciar `npm run start:dev`.
