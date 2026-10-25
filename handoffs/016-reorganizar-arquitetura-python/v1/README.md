# 016/v1 — Composition root do serviço Python

- Versão: `v1`; versão-base: `015` verificada; data: 2026-10-25 -03:00; status: `verified`.
- Aplicação: `/home/dev/dev/ia/rastro-ai/rastro-ai`; arquivos conferidos: `src/rastro_ai/indexing.py`, `src/rastro_ai/retrieval.py`, `src/rastro_ai/document_indexing/**`, `tests/test_runtime_vector_store.py` e `pyproject.toml`.
- Reconciliação: `015` já havia criado portas e adapters, mas `retrieval.py` ainda inicializava o vector store durante o import; `indexing.py` mantinha casos de uso globais.
- Decisão: criar `rastro_ai.bootstrap.container` como composition root inicial, preservar fachadas públicas e adiar remoções/renomeações para etapas posteriores.

## O que foi feito

- Criado `rastro-ai/src/rastro_ai/bootstrap/container.py`, com `IndexingContainer`, `RetrievalContainer`, `build_indexing_container()` e `build_retrieval_container()`.
- Alterado `src/rastro_ai/indexing.py`: as fachadas agora obtêm extractor, chunker e caso de uso pelo container, sem instâncias globais.
- Alterado `src/rastro_ai/retrieval.py`: a seleção do backend PostgreSQL e a composição dos casos de uso foram movidas para o container.
- Alterado `tests/test_runtime_vector_store.py`: importação segura passou a ser coberta separadamente da validação do backend configurado.
- O problema resolvido foi o acoplamento entre importação de módulo e configuração/recursos externos, mantendo a validação obrigatória do runtime vetorial.

## O que muda na aplicação

- `import rastro_ai.retrieval` não tenta mais selecionar ou conectar o vector store; o erro de configuração ocorre quando o container ou uma fachada de retrieval é executado.
- Indexação, retrieval e resposta continuam usando os mesmos contratos, adapters, PGVector, embeddings, filtros por projeto e resultados.
- O runtime permanece síncrono e a API pública existente é preservada; não houve deploy, migração de banco, mudança de modelo, prompt ou avaliação semântica.
- Risco conhecido: a construção atual ainda recria dependências por operação e os namespaces `document_indexing`, `document_ingestion` e `semantic_search` continuam coexistindo; isso será tratado em etapas posteriores.
- Fora do escopo: remoção de aliases, criação de worker, ativação do LangGraph, mudança do endpoint HTTP e integração com Langfuse/DeepEval.

## Jornada da aplicação nesta versão

Antes, importar a fachada de retrieval já construía o backend vetorial e podia falhar antes de qualquer chamada. Agora, o serviço importa suas interfaces sem inicializar infraestrutura e compõe o backend somente quando o fluxo de indexação ou consulta é executado. Para a pessoa usuária, o resultado funcional permanece igual; a evolução futura poderá montar containers diferentes para runtime, testes, workers e evaluation.

## Como usar e validar a aplicação nesta versão

Na aplicação `rastro-ai/`, o uso público continua sendo `rastro_ai.indexing.index_document(...)`, `rastro_ai.indexing.index_document_in_store(...)`, `rastro_ai.retrieval.retrieve_chunks(...)` e `rastro_ai.retrieval.answer_question(...)`. Para validar apenas a importação, execute `PYTHONPATH=src python -c "import rastro_ai.retrieval; print('import ok')"`; para executar retrieval real, configure `VECTOR_STORE_BACKEND=postgres`, `DATABASE_URL` e `OPENAI_API_KEY` conforme o README da aplicação.

## Cobertura por comportamento

- Composição de indexação: os testes existentes de `tests/test_indexing.py` continuam exercitando extração, chunking, offsets e fachada pública; resultado esperado: comportamento preservado.
- Importação segura: `tests/test_runtime_vector_store.py::test_import_does_not_build_vector_store` confirma que ausência de configuração não impede import; resultado esperado: processo `0`.
- Validação do runtime: os testes de configuração ausente e modo lexical chamam `build_retrieval_container()`; resultado esperado: falha explícita com `VECTOR_STORE_BACKEND must be 'postgres'`.
- Evaluation: `evals/evaluate.py` permanece determinística e deve continuar em `20/20`; smoke API → Python → PostgreSQL não foi executado nesta rodada.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: resultado, 36 testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -m evals.evaluate`: resultado, `20/20` casos aprovados e métricas `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src env -u VECTOR_STORE_BACKEND .venv/bin/python -c "import rastro_ai.retrieval; print('import ok')"`: resultado, `import ok` sem exigir `VECTOR_STORE_BACKEND`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: resultado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/016-reorganizar-arquitetura-python/README.md handoffs/016-reorganizar-arquitetura-python/TIMELINE.md handoffs/016-reorganizar-arquitetura-python/v1/README.md handoffs/016-reorganizar-arquitetura-python/v1/TIMELINE.md`: resultado, `handoffs válidos: 4 arquivo(s)`.
