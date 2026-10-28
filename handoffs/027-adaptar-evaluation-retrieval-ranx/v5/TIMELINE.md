# Timeline — 027/v5 organização explícita do fluxo

## 2026-10-27 23:55 -03:00 — aplicação da v5

- Status: `applied`.
- Arquivo real alterado: `rastro-ai/evals/retrieval/evaluate.py`.
- Mudanças: imports explícitos e helpers separados para acumuladores, invariantes, ranking e agregação; comentários de fluxo adicionados.
- Contrato preservado: nomes públicos, métricas calculadas e formato consumido por `report.py` permanecem iguais.
- Verificação: compilação, `git diff --check` e suíte controlada executados; 6 testes terminaram com `OK`.
- Limite: evaluation real contra PGVector não executada; finalização aguarda comando explícito.
