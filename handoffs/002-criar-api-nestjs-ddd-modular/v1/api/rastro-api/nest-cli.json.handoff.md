## Alteração: configuração do Nest CLI

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/nest-cli.json`
- Aplicação: `api`
- Localização: arquivo novo na raiz da aplicação
- Operação: `insert`
- Âncoras: arquivo inexistente.
- Motivo: indicar a raiz do código e o arquivo TypeScript usado no build.
- Impacto: padroniza `nest build` e a saída de compilação.
- Pré-requisitos: `tsconfig.build.json`.

### Código copiável

```json
{
  "$schema": "https://json.schemastore.org/nest-cli",
  "collection": "@nestjs/schematics",
  "sourceRoot": "src",
  "compilerOptions": {
    "deleteOutDir": true,
    "webpack": false,
    "tsConfigPath": "tsconfig.build.json"
  }
}
```

### Verificação

`npx nest info` deve reconhecer `src` como source root.
