# Linha do tempo — 008 v1 Dataset e baseline determinístico

## Registro da aplicação

- Data/hora: 2026-10-24 -03:00 | Status: `proposed`.
- Arquivos reais conferidos: indexação, retrieval, resposta, testes, README da IA e referências da Fase 1.
- Mudanças previstas: dataset de 20 casos, evaluator determinístico, baseline versionado, testes e documentação de uso.
- Problema: inexistência de uma referência repetível para regressões de retrieval, citações, ausência de evidência e isolamento.
- Pendências: DeepEval, LLM-as-judge, CI dedicado e métricas de custo/latência dependem de etapas posteriores.
- Verificação prevista: 18 testes, runner com 20 casos, compilação e hook estrito.

## Verificação da rodada

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos conferidos: artefatos `evals`, testes, README da IA e quatro registros desta implementação.
- Resultado: 18 testes aprovados; `20/20` casos; `source_recall`, `citation_precision`, `safe_abstention` e `project_isolation` em `1.0`.
- Verificações adicionais: `compileall` sem erro e `validate-handoffs.sh` estrito com quatro arquivos válido.
- Pendência: finalização explícita ainda necessária; `CURRENT.md` permanece em `008`.

## Finalização — v1 verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Resultado: critérios da implementação atendidos sem alteração adicional no runtime.
- Verificação: 18 testes, baseline `20/20`, quatro métricas `1.0`, compilação e hook estrito passaram.
- Avanço: `CURRENT.md` será atualizado para `009` após a atualização da sequência.
- Commit: `9efd2d2` — `Finalizar baseline de evaluation`.
