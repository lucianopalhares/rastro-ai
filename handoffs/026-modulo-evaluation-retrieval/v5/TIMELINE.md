# Timeline — 026/v5 golden dataset único

## 2026-10-27 -03:00 — aplicação v5

- Status: `applied`.
- Versão-base: `v4` aplicada; datasets, runners, testes e referências foram conferidos antes da migração.
- Mudanças: criado `evals/dataset/golden.json`; dois runners usam o mesmo schema; arquivos duplicados removidos.
- Evidência: 45 testes no container e baseline determinístico `20/20` aprovados; hook estrutural aprovado.
- Pendência: avaliação integrada de retrieval contra PGVector real continua não executada.
