## Alteração: configuração de build

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/tsconfig.build.json`
- Aplicação: `api`
- Localização: arquivo novo na raiz da aplicação
- Operação: `insert`
- Âncoras: arquivo inexistente.
- Motivo: excluir testes e artefatos de desenvolvimento do bundle de produção.
- Impacto: o build produz somente o runtime da API em `dist`.
- Pré-requisitos: `tsconfig.json`.

### Código copiável

```json
{
  "extends": "./tsconfig.json",
  "exclude": ["node_modules", "dist", "test", "**/*.spec.ts"]
}
```

### Verificação

`npm run build` deve gerar `dist/main.js`.
