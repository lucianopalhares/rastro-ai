# 008 — Evaluation baseline
- Data/hora: 2026-10-24 -03:00 | Status: `verified` | Aplicação: IA (`rastro-ai`).
- Dependência/ordem: `007` verificada; etapa 6 da Fase 1; antecede `009` e `010`.
- Objetivo: versionar dataset mínimo e baseline reproduzível para retrieval, respostas e citações.
- Evolução: `v1` criou 20 casos, evaluator determinístico, testes e baseline JSON executado.
- Impacto: mede o comportamento lexical/extrativo atual sem LLM, rede, DeepEval ou custo de inferência.
- Critério: dataset carregável, todos os casos avaliados e métricas reproduzidas pelos testes; verificado.
- Pendências: DeepEval, métricas LLM-as-judge, integração API e smoke pós-deploy permanecem futuras.
- Pasta: `handoffs/008-evaluation-baseline/` | Próxima ação: iniciar `009-observabilidade-e-custo`.
