## Alteração: imagem de produção da API

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-ai/Dockerfile`
- Aplicação: `api`
- Operação: `replace`
- Âncoras: substituir o conteúdo atual do arquivo.
- Motivo: manter uma imagem de produção independente da imagem de desenvolvimento.
- Impacto: imagem multi-stage com dependências reproduzíveis e apenas runtime na etapa final.
- Pré-requisitos: `package-lock.json` versionado, `package.json`, `tsconfig.build.json` e `src/`.

### Código copiável

```dockerfile
FROM node:22-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM dependencies AS builder
COPY tsconfig*.json nest-cli.json ./
COPY src ./src
RUN npm run build
RUN npm prune --omit=dev

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Verificação

Executar `cd rastro-ai && npm install` uma vez para gerar e versionar `package-lock.json`. Depois, `docker build -f rastro-ai/Dockerfile -t rastro-api:production rastro-ai` deve concluir.
