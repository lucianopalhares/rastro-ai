# v1 — Dataset e baseline determinístico

- Versão: `v1` | Versão-base: `007/v1` (`verified`) | Data: 2026-10-24 -03:00 | Status: `verified`.
- Contexto: o fluxo real já indexa chunks, recupera por projeto e responde com citações, mas não tinha evaluation versionado.
- Arquivos reais a alterar: `/home/dev/dev/ia/rastro-ai/rastro-ai/evals/dataset.json`, `evaluate.py`, `__init__.py`, `baseline.json`, `README.md`, `tests/test_evaluation.py` e `rastro-ai/README.md`.
- Operação: `insert` dos artefatos e testes; âncoras `EVALUATION_DATASET`, `run_evaluation` e seção de evaluation da aplicação.

## O que foi feito

- Foi criado dataset com 20 casos cobrindo resposta direta, múltiplos trechos, ausência, conflito, citações, isolamento e prompt injection em documento.
- Foi criado evaluator determinístico que usa as fachadas reais, calcula cobertura de fontes, ausência segura, correção das citações e isolamento por projeto, e compara `baseline.json` sem data volátil.
- Problema resolvido: estabelecer uma referência reproduzível para o comportamento atual antes de introduzir LLM, embeddings ou observabilidade.

## O que muda na aplicação

- A aplicação passa a ter uma suíte de evaluation local e artefatos versionados; o runtime de indexação, retrieval e resposta não muda.
- O baseline mede apenas contratos determinísticos e não afirma qualidade semântica, faithfulness ou relevância julgada por LLM.
- DeepEval, API, frontend, worker, persistência e smoke pós-deploy ficam fora do escopo; futuras mudanças de IA devem comparar seus resultados com este baseline.

## Jornada da aplicação nesta versão

- Antes: o fluxo respondia localmente, mas não havia conjunto curado para repetir e comparar seu comportamento.
- Agora: casos representativos podem ser executados contra indexação, retrieval e resposta reais, com resultado JSON estável.
- Resultado percebido: a equipe consegue detectar quebra de fontes, isolamento ou negativa de evidência antes de evoluir o sistema.
- Próxima evolução: integrar métricas semânticas, DeepEval e execução no CI quando houver resposta generativa e observabilidade.

## Como usar e validar a aplicação nesta versão

- Caminho disponível: na raiz `rastro-ai/`, executar `python3 -m unittest discover -s tests -v` e `python3 -m evals.evaluate`.
- Uso pelo produto completo: indisponível; não existe endpoint ou tela para executar evaluations.
- Resultado observado: 18 testes aprovados e o runner informou 20 casos aprovados com métricas 1.0.

## Cobertura por comportamento

| Comportamento | Teste unitário/contrato | Integração ou smoke/manual real | Resultado esperado |
| --- | --- | --- | --- |
| Dataset cobre categorias mínimas | `tests/test_evaluation.py::test_dataset_has_twenty_cases_and_required_categories` | `python3 -m evals.evaluate` | 20 casos e todas as categorias obrigatórias presentes |
| Retrieval encontra fontes esperadas | `tests/test_evaluation.py::test_evaluation_reproduces_baseline` | Runner contra `index_chunks`/`retrieve_chunks` reais | `source_recall` igual a `1.0` |
| Resposta preserva citações válidas | `tests/test_evaluation.py::test_evaluation_reproduces_baseline` | Runner contra `answer_question` real | `citation_precision` igual a `1.0` |
| Ausência e isolamento são seguros | `tests/test_evaluation.py::test_evaluation_reproduces_baseline` | Casos sem evidência e projeto adversário no runner | `safe_abstention` e `project_isolation` iguais a `1.0` |

## Instruções de validação

1. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m unittest discover -s tests -v`; resultado esperado: 18 testes aprovados.
2. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src python3 -m evals.evaluate`; resultado esperado: 20 casos aprovados e métricas do baseline reproduzidas.
3. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m compileall -q src tests evals`; resultado esperado: conclusão sem erro.
4. Execute `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/008-evaluation-baseline/README.md handoffs/008-evaluation-baseline/TIMELINE.md handoffs/008-evaluation-baseline/v1/README.md handoffs/008-evaluation-baseline/v1/TIMELINE.md`; resultado esperado: `handoffs válidos: 4 arquivo(s)`.
