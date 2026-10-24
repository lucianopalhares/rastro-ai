## Alteração: manifesto da API

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/package.json`
- Aplicação: `api`
- Localização: arquivo novo na raiz da aplicação
- Operação: `insert`
- Âncoras: arquivo inexistente; criar como primeiro arquivo da aplicação.
- Motivo: declarar NestJS 12, TypeScript, validação HTTP e scripts de desenvolvimento/build.
- Impacto: habilita instalação e execução padronizadas; não contém segredos nem conexão automática com banco.
- Pré-requisitos: nenhum.

### Código copiável

```json
{
  "name": "rastro-api",
  "version": "0.1.0",
  "private": true,
  "license": "UNLICENSED",
  "scripts": {
    "build": "nest build",
    "format": "prettier --write \"src/**/*.ts\"",
    "start": "nest start",
    "start:dev": "nest start --watch",
    "start:prod": "node dist/main.js",
    "test": "jest --passWithNoTests --runInBand"
  },
  "dependencies": {
    "@nestjs/common": "^12.2.0",
    "@nestjs/config": "^12.0.1",
    "@nestjs/core": "^12.2.0",
    "@nestjs/platform-express": "^12.2.0",
    "class-transformer": "^0.5.1",
    "class-validator": "^0.15.1",
    "reflect-metadata": "^0.2.2",
    "rxjs": "^7.8.2"
  },
  "devDependencies": {
    "@nestjs/cli": "^12.0.10",
    "@nestjs/schematics": "^12.0.5",
    "@nestjs/testing": "^12.2.0",
    "@types/express": "^5.0.3",
    "@types/jest": "^30.0.0",
    "@types/node": "^24.9.1",
    "@typescript-eslint/eslint-plugin": "^8.46.2",
    "@typescript-eslint/parser": "^8.46.2",
    "eslint": "^9.38.0",
    "eslint-config-prettier": "^10.1.8",
    "eslint-plugin-prettier": "^5.5.4",
    "jest": "^30.2.0",
    "prettier": "^3.6.2",
    "source-map-support": "^0.5.21",
    "ts-jest": "^29.4.5",
    "ts-loader": "^9.5.4",
    "ts-node": "^10.9.2",
    "tsconfig-paths": "^4.2.0",
    "typescript": "^5.9.3"
  }
}
```

### Verificação

Executar na raiz de `rastro-api`: `npm install`, `npm run build` e `npm test`.
