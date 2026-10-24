# v7 — Reconhecer globais do Jest no TypeScript

- Versão-base: `v6`; a configuração do Jest já está presente, mas o `tsconfig.json` real ainda não inclui os tipos globais.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivo conferido: `/home/dev/dev/ia/rastro-ai/rastro-api/tsconfig.json`.
- Reconciliação: `@types/jest`, `jest` e `ts-jest` estão instalados; `npx tsc --noEmit` reproduz o erro, enquanto `--types node,jest` passa.
- Operação: `replace` do arquivo completo; inserir `compilerOptions.types` com `node` e `jest`.
- Âncora: chave `compilerOptions` do `tsconfig.json`; JSON não aceita comentários, e a exceção fica registrada aqui.
- Impacto: `describe`, `it` e `expect` passam a ser reconhecidos no TypeScript e pelo `ts-jest`, sem alterar o código de produção.
- Ordem/verificação: aplicar após `v6`; executar `docker compose run --rm --no-deps api npm test -- --runInBand` e `docker compose run --rm --no-deps api npm run build`.
