# 002 — Compatibilizar TypeScript 6

Versão: `v3` | Versão-base: `v2` | Data/hora: 2026-10-23 -03:00 | Status: `proposed`
Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/rastro-ai/tsconfig.json`, `tsconfig.build.json`; a aplicação real ainda não contém as opções propostas na v1.
Reconciliação: os dois erros do watch correspondem integralmente à pendência histórica de `rootDir` e `ignoreDeprecations`; nenhum trecho foi considerado aplicado.
Pendência: aplicar `api/tsconfig.json`; `tsconfig.build.json` permanece inalterado porque já estende o arquivo base.
Ordem: aplicar o handoff e executar build/watch; critério: ausência de `TS5011` e `TS5101`, com saída em `dist`.
