# 017/v1 — Renomear fluxo de extração e chunking

- Versão: `v1`; versão-base: `016` verificada; data: 2026-10-25 -03:00; status: `verified`.
- Aplicação: `/home/dev/dev/ia/rastro-ai/rastro-ai`; arquivos conferidos: fachada `indexing.py`, container, caso de uso, serviço HTTP, exports, testes, README e documento arquitetural.
- Reconciliação: `index_document()` apenas extraía e gerava chunks; `index_document_in_store()` executava também persistência; `IndexDocumentUseCase` e `index_document.py` mantinham a mesma ambiguidade.
- Decisão: usar `extract_and_chunk_document`, `index_document_chunks`, `ExtractAndChunkDocumentUseCase` e `extract_and_chunk_document.py`, sem aliases antigos para evitar dois vocabulários ativos.

## O que foi feito

- Renomeado o módulo real para `rastro-ai/src/rastro_ai/document_indexing/application/use_cases/extract_and_chunk_document.py` e a classe para `ExtractAndChunkDocumentUseCase`.
- Renomeadas as fachadas públicas em `rastro-ai/src/rastro_ai/indexing.py`: `extract_and_chunk_document()` representa extração/chunking e `index_document_chunks()` representa o fluxo completo até persistência.
- Atualizados `bootstrap/container.py`, `service.py`, `rastro_ai/__init__.py`, `document_indexing/__init__.py` e `application/use_cases/__init__.py`.
- Atualizados testes, README da aplicação e `docs/architecture/document-upload-indexing-flow.md` para usar os nomes novos.
- O problema resolvido foi a diferença entre o significado do nome “index document” e o comportamento real de geração de chunks.

## O que muda na aplicação

- `extract_and_chunk_document()` extrai texto e gera `DocumentChunk`, sem embeddings ou persistência.
- `index_document_chunks()` chama a etapa anterior e então executa `retrieval.index_chunks()`, embeddings e PGVector.
- O endpoint HTTP continua recebendo o mesmo payload e retornando o mesmo contrato; apenas o método interno chamado pelo serviço mudou.
- Não foram alteradas estratégia de chunking, offsets, metadados, embeddings, banco, evaluation ou custo/latência esperados.
- Risco conhecido: consumidores externos que importavam `index_document`, `index_document_in_store` ou `IndexDocumentUseCase` precisam migrar para os nomes novos; aliases antigos não foram preservados.

## Jornada da aplicação nesta versão

Antes, o nome `index_document()` parecia indicar indexação completa, mas realizava apenas extração e chunking. Agora, os nomes distinguem a preparação dos chunks da persistência vetorial, tornando o fluxo compreensível para futuras etapas de orquestração e evaluation. O upload continua produzindo o mesmo resultado e o documento continua sendo persistido no PGVector.

## Como usar e validar a aplicação nesta versão

Use `rastro_ai.indexing.extract_and_chunk_document(document_id, path, project_id=...)` para obter chunks sem persistência. Use `rastro_ai.indexing.index_document_chunks(document_id, path, project_id=...)` ou o endpoint existente `POST /index` para executar o fluxo completo com embeddings e PGVector. O payload HTTP e a requisição de upload documentados em `docs/architecture/document-upload-indexing-flow.md` permanecem iguais.

## Cobertura por comportamento

- Extração e chunking: `tests/test_indexing.py::test_extract_and_chunk_document_extracts_and_chunks_fixture`, `test_use_case_depends_on_extractor_port` e `test_use_case_delegates_chunking_to_port` cobrem o novo nome e o contrato preservado.
- Persistência: `tests/test_indexing.py::test_index_document_chunks_persists_chunks` e `tests/test_service.py::ServiceTests` cobrem o fluxo até o boundary HTTP/persistência.
- Regressão: a suíte completa e `evals/evaluate.py` devem permanecer aprovadas; smoke API → Python → PGVector real não faz parte desta rodada.
- Referências: busca por `index_document_in_store`, `IndexDocumentUseCase` e chamadas antigas deve retornar somente histórico documental, se houver.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: resultado, 36 testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -m evals.evaluate`: resultado, `20/20` casos aprovados e métricas `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: resultado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && rg -n 'index_document_in_store|IndexDocumentUseCase|from .*index_document import' rastro-ai docs/architecture --glob '*.py' --glob '*.md'`: resultado, nenhuma referência ativa aos nomes antigos.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -c "from rastro_ai import extract_and_chunk_document, index_document_chunks; from rastro_ai.document_indexing import ExtractAndChunkDocumentUseCase; print('renamed imports ok')"`: resultado, imports novos carregados.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/017-renomear-fluxo-extracao-chunking/README.md handoffs/017-renomear-fluxo-extracao-chunking/TIMELINE.md handoffs/017-renomear-fluxo-extracao-chunking/v1/README.md handoffs/017-renomear-fluxo-extracao-chunking/v1/TIMELINE.md`: resultado esperado, handoffs válidos.
