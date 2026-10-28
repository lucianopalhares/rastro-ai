# 026/v1 — Módulo de evaluation de retrieval

- Versão: `v1`; versão-base: implementação `025` verificada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: runtime já retorna `RetrievedChunk` com `document_id`, índice, projeto e score; evaluation existente usa store lexical em memória.
- Escopo autorizado: adicionar evaluator isolado, golden dataset, testes sem rede e comando de integração contra a fachada PGVector.
- Invariantes: não alterar runtime; nenhum teste unitário chama OpenAI, PostgreSQL ou Langfuse; IDs do golden usam `document_id:index`.

## O que foi feito

- Criado `evals/retrieval/evaluate.py` com loader, contrato injetável e métricas Recall@k, Precision@k, MRR, nDCG, isolamento, ordenação de score e abstinência.
- Criado golden dataset com casos de fato direto, paráfrase, múltiplas evidências, ausência de evidência e isolamento.
- Criado teste determinístico com resultados fake para provar ranking e invariantes sem fingir integração com PGVector.

## O que muda na aplicação

- A aplicação de runtime não muda; a nova capacidade permite medir os chunks retornados antes de avaliar respostas de LLM.
- O comando `python -m evals.retrieval.evaluate` chama a fachada real somente quando executado com banco, embeddings e corpus configurados.
- O dataset inicial é um contrato de avaliação e exige que os documentos/chunks correspondentes estejam previamente indexados para produzir métricas úteis.
- Fora do escopo: DeepEval, geração de respostas, criação automática de corpus, alteração de threshold ou mudança no ranking do PGVector.

## Jornada da aplicação nesta versão

Antes, os testes cobriam principalmente o adapter e um ranking lexical em memória. Agora, existe um evaluator que compara o ranking do retrieval com chunks esperados, sem misturar a geração da resposta.

## Como usar e validar a aplicação nesta versão

1. Indexe no projeto indicado os documentos que geram os IDs `meeting-db:0`, `meeting-cache:0` e `project-a-decision:0`.
2. Configure `VECTOR_STORE_BACKEND=postgres`, `DATABASE_URL` e `OPENAI_API_KEY` no ambiente do `ai-indexer`.
3. Execute `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate --dataset evals/retrieval/dataset.json --ks 1,3,5` dentro de `rastro-ai`.
4. Confira o JSON: `Recall@k`, `Precision@k`, `MRR`, `nDCG`, `project_isolation`, `score_ordering` e `abstention` devem refletir o corpus anotado; o caso sem evidência pode revelar que o runtime ainda não possui threshold de abstinência.

A integração real com PGVector não é executada automaticamente nos testes unitários: ela depende de banco, embeddings, documentos indexados e credenciais configurados pelo responsável.

## Cobertura por comportamento

- Contrato e métricas: `tests/test_retrieval_evaluation.py`, sem rede; deve calcular ranking, cobertura e posição.
- Isolamento, score e ausência: `tests/test_retrieval_evaluation.py`; deve reportar violações sem alterar o retriever.
- Integração PGVector: comando manual documentado; não executada automaticamente nesta rodada porque depende de corpus, banco e chave configurados.

## Instruções de validação

- `PYTHONPATH=src:. python3 -m unittest -q tests.test_retrieval_evaluation`: esperado, todos os testes do módulo aprovados sem rede.
- `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate --dataset evals/retrieval/dataset.json --ks 1,3,5`: esperado, JSON agregado e diagnóstico por caso contra o PostgreSQL/PGVector configurado.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md`: esperado, quatro handoffs válidos.
