# 016/v2 — Remoção de duplicações e componentes não utilizados

- Versão: `v2`; versão-base: `016/v1` verificada; data: 2026-10-25 -03:00; status: `verified`.
- Aplicação: `/home/dev/dev/ia/rastro-ai/rastro-ai`; arquivos reais conferidos: todos os módulos Python em `src/rastro_ai`, testes, evaluation, `pyproject.toml`, Dockerfiles e Compose.
- Reconciliação: `v1` havia criado o composition root, mas aliases sem consumidores internos continuavam duplicando `document_indexing`; `SentenceTransformerEmbeddingProvider` só era exportado pelo próprio pacote e a biblioteca não estava declarada.
- Decisão: manter `document_indexing` como namespace canônico atual, preservar `indexing.py`, `retrieval.py` e `service.py`, e remover somente duplicações sem uso interno confirmado.

## O que foi feito

- Removidos os pacotes duplicados `chunking`, `document_ingestion`, `documents`, `embeddings` e `semantic_search`, que apenas reexportavam implementações de `document_indexing` ou não tinham consumidores internos.
- Removido `rastro-ai/src/rastro_ai/document_indexing/infrastructure/embeddings/sentence_transformer.py` e seu reexport; o runtime usa exclusivamente `OpenAIEmbeddingRepository` e a dependência Sentence Transformers não estava declarada.
- Alterados `rastro_ai/__init__.py`, `indexing.py`, `retrieval.py` e o README da aplicação para apontar diretamente para o namespace canônico e documentar a migração.
- O problema resolvido foi a existência de múltiplos caminhos de importação para as mesmas entidades, portas, casos de uso e adapters.

## O que muda na aplicação

- O fluxo interno continua usando extração, chunking LangChain, embeddings OpenAI, PGVector, retrieval, evaluation e entrypoint HTTP sem mudança comportamental.
- Imports internos antigos como `rastro_ai.semantic_search...` e `rastro_ai.chunking...` deixam de existir; consumidores devem usar `rastro_ai.indexing`, `rastro_ai.retrieval` ou `rastro_ai.document_indexing...`.
- A superfície do pacote ficou menor e a documentação passa a refletir apenas o namespace canônico atual.
- Risco conhecido: código externo não pesquisado no repositório pode depender dos aliases removidos; não há evidência de consumidores internos.
- Fora do escopo: remover o namespace `document_indexing`, mover workflows LangGraph ou reorganizar `evals/`.

## Jornada da aplicação nesta versão

Antes, a mesma capacidade podia ser importada por vários namespaces que apontavam para os mesmos arquivos, e havia um provider local não utilizado. Agora, a aplicação possui um caminho canônico dentro de `document_indexing`, enquanto as fachadas públicas preservam o uso principal. O upload e a evaluation continuam com o mesmo comportamento; a mudança é estrutural e pode exigir migração de consumidores externos.

## Como usar e validar a aplicação nesta versão

Use `rastro_ai.indexing.index_document(...)` ou `rastro_ai.indexing.index_document_in_store(...)` para indexação, `rastro_ai.retrieval.retrieve_chunks(...)` ou `answer_question(...)` para consulta e `python -m rastro_ai.service` para o entrypoint HTTP. Não use mais imports `rastro_ai.chunking`, `rastro_ai.document_ingestion`, `rastro_ai.documents`, `rastro_ai.embeddings` ou `rastro_ai.semantic_search`; o equivalente interno está em `rastro_ai.document_indexing`.

## Cobertura por comportamento

- Imports canônicos: `tests/test_indexing.py`, `tests/test_answers.py`, `tests/test_retrieval.py` e `tests/test_langchain_pipeline.py` continuam carregando as implementações canônicas; evidência unitária/contratual: suíte `unittest`; resultado: testes aprovados.
- Runtime: `tests/test_service.py` mantém o endpoint e `tests/test_runtime_vector_store.py` mantém a validação do backend; evidência unitária/contratual: `ServiceTests` e `RuntimeVectorStoreTests`; resultado: comportamento preservado.
- Evaluation: `evals/evaluate.py` continua usando `document_indexing` diretamente; resultado: `20/20` casos aprovados.
- Referências residuais: busca por `rastro_ai.chunking`, `document_ingestion`, `documents`, `embeddings`, `semantic_search` e `SentenceTransformerEmbeddingProvider` não encontrou referências Python internas.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: resultado, 36 testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -m evals.evaluate`: resultado, `20/20` casos aprovados e métricas `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: resultado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && rg -n 'rastro_ai\\.(chunking|document_ingestion|documents|embeddings|semantic_search)|SentenceTransformerEmbeddingProvider|sentence_transformer' rastro-ai --glob '*.py' --glob '!**/__pycache__/**'`: resultado, nenhuma referência interna.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -c "import rastro_ai, rastro_ai.indexing, rastro_ai.retrieval, rastro_ai.document_indexing, rastro_ai.bootstrap.container"`: resultado, imports canônicos carregados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -c "import importlib; names=['rastro_ai.chunking','rastro_ai.document_ingestion','rastro_ai.documents','rastro_ai.embeddings','rastro_ai.semantic_search','rastro_ai.document_indexing.infrastructure.embeddings.sentence_transformer']; [importlib.import_module(name) for name in names]"`: resultado esperado, `ModuleNotFoundError` para cada alias removido.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/016-reorganizar-arquitetura-python/README.md handoffs/016-reorganizar-arquitetura-python/TIMELINE.md handoffs/016-reorganizar-arquitetura-python/v1/README.md handoffs/016-reorganizar-arquitetura-python/v1/TIMELINE.md handoffs/016-reorganizar-arquitetura-python/v2/README.md handoffs/016-reorganizar-arquitetura-python/v2/TIMELINE.md`: resultado esperado, handoffs válidos.
