# Timeline — 027/v2 separação entre ranking e invariantes

## 2026-10-27 22:15 -03:00 — aplicação da v2

- Status: `applied`.
- Arquivos reais conferidos: módulos de métricas, `metrics/__init__.py`, evaluator, testes e README do retrieval.
- Mudanças: módulos movidos para `ranking/` e `invariants/`; imports públicos preservados; distinção documentada.
- Pendência: repetir compilação, suíte controlada e hook estrutural.

## 2026-10-27 22:30 -03:00 — evidência da v2

- Status: `applied`.
- Evidência: compilação Python, `git diff --check`, hook estrutural e `./rastro-ai/evals/retrieval/run_evaluation.sh test` concluídos.
- Resultado: 6 testes terminaram com `OK`; os imports públicos continuam compatíveis.
- Limite: evaluation real PGVector não executada; finalização e commit aguardam comando explícito.
