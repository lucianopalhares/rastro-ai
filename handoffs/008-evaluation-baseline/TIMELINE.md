# Linha do tempo — 008 Evaluation baseline

## v1 — Dataset e baseline determinístico

- Data/hora: 2026-10-24 -03:00 | Status: `proposed`.
- Arquivos reais previstos: `rastro-ai/evals/`, testes de evaluation e README da aplicação.
- Objetivo: medir retrieval, ausência de evidência, fontes esperadas, citações válidas e isolamento por projeto.
- Escopo: 20 casos versionados e evaluator sem modelo, mantendo DeepEval e integração externa fora da rodada.
- Verificação prevista: testes da suíte, execução do baseline, compilação e hook estrito.
- Pendências: comparar futuras mudanças de modelo, prompt, embeddings ou grafo contra este baseline.

## v1 — Aplicação concluída

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: `rastro-ai/evals/dataset.json`, `evaluate.py`, `__init__.py`, `baseline.json`, `README.md`, `tests/test_evaluation.py` e `rastro-ai/README.md`.
- Mudanças aplicadas: 20 casos, executor determinístico, quatro métricas, baseline estável, quatro testes e documentação.
- Problema resolvido: evaluation repetível para fontes, citações, ausência de evidência e isolamento por projeto.
- Verificação: 18 testes, 20/20 casos, métricas 1.0, compilação e hook estrito passaram.
- Pendências: status final e avanço de `CURRENT.md` dependem da finalização explícita da tarefa.

## Finalização — v1 verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Arquivos reais e quatro arquivos de handoff conferidos; nenhuma divergência ou pendência bloqueadora encontrada.
- Verificação: 18 testes, 20/20 casos, quatro métricas em `1.0`, compilação, `git diff --check` e hook estrito passaram.
- Resultado: implementação 008 encerrada; `CURRENT.md` avança para `009` conforme a sequência.
- Commit: `9efd2d2` — `Finalizar baseline de evaluation`.
- Verificação do commit: lista explícita de 14 arquivos, diff sem erros e status da implementação encerrado.
