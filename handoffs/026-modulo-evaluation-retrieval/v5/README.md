# 026/v5 — Golden dataset único

- Versão: `v5`; versão-base: `026/v4` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: havia `evals/dataset.json` para o baseline e `evals/retrieval/dataset/golden.json` para retrieval, com schemas diferentes.
- Escopo autorizado: consolidar os dois em `rastro-ai/evals/dataset/golden.json`, migrar runners/testes e remover duplicações.
- Invariantes: 20 casos e baseline 20/20 preservados; retrieval usa `relevant_chunks`; resposta futura usa `expected_answer`; runtime não muda.
- Arquivos reais conferidos: ambos datasets, dois runners, testes, README de evals e referências do módulo retrieval.

## O que foi feito

- Criado um golden único com schema `rastro-ai.golden.v1`, contendo query, projeto, documentos, chunks relevantes e expectativa opcional de resposta.
- `evals/evaluate.py` e `evals/retrieval/evaluate.py` passaram a consumir o mesmo arquivo; testes antigos e novos foram migrados.
- Removidos os dois arquivos duplicados anteriores e atualizada a documentação de evaluation.

## O que muda na aplicação

- Existe uma única fonte de verdade para os casos de evaluation.
- O retrieval usa `relevant_chunks` e suas relevâncias; o baseline extrativo usa `expected_answer.source_document_ids` e `abstain`.
- `expected_answer.text` e `must_contain` ficam preparados para futura avaliação determinística/DeepEval, mas nenhum LLM foi adicionado.
- Fora do escopo: geração de resposta, DeepEval, alteração de métricas, threshold e PGVector.

## Jornada da aplicação nesta versão

Antes, era necessário escolher entre dois datasets com contratos diferentes. Agora, ambos os fluxos leem o mesmo caso: retrieval avalia chunks e o fluxo de resposta avalia fontes/abstinência; a resposta semântica futura poderá usar os campos opcionais.

## Como usar e validar a aplicação nesta versão

Use `rastro-ai/evals/dataset/golden.json` como único arquivo de casos. Execute `PYTHONPATH=src python3 -m evals.evaluate` para o baseline extrativo ou `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate` para retrieval; o segundo exige PGVector, embeddings e documentos indexados.

## Cobertura por comportamento

- Schema único: `tests/test_evaluation.py` e `tests/test_retrieval_evaluation.py` cobrem 20 casos e campos de ambos os fluxos.
- Baseline de resposta: 20/20 casos e métricas determinísticas aprovados no container.
- Retrieval: evaluator e métricas cobertos sem rede; integração PGVector real permanece manual.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer sh -lc 'python -m unittest discover -s tests -p "test*.py" -q && python -m evals.evaluate'`: esperado, 45 testes aprovados e baseline `20/20`.
- `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate --dataset evals/dataset/golden.json --ks 1,3,5`: esperado, JSON de retrieval contra PGVector configurado; não executado automaticamente por depender de corpus e credenciais.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md`: esperado, doze handoffs válidos.
