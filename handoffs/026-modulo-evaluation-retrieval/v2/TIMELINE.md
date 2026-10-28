# Timeline — 026/v2 métricas desacopladas de retrieval

## 2026-10-27 -03:00 — aplicação v2

- Status: `applied`.
- Versão-base: `v1` aplicada; código real relido antes da alteração e runtime preservado.
- Mudanças: sete métricas extraídas para módulos puros; evaluator passou a apenas orquestrar e agregar.
- Evidência: 4 testes específicos, 45 testes Python no container e `git diff --check` aprovados.
- Pendência: validar o comando integrado contra PGVector com corpus anotado; nenhuma integração externa foi executada nesta rodada.
