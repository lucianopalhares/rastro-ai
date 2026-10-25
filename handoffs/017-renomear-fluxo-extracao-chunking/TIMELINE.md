## v1 — Renomeação aplicada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai`; versão-base: implementação `016` verificada; referências reais conferidas antes da alteração.
- Mudanças: `IndexDocumentUseCase` virou `ExtractAndChunkDocumentUseCase`; `index_document()` virou `extract_and_chunk_document()`; `index_document_in_store()` virou `index_document_chunks()`; módulo, container, serviço, testes, README e arquitetura foram atualizados.
- Problema resolvido: o nome `index_document()` sugeria persistência, embora gerasse somente texto e chunks.
- Impacto: API programática interna e exports públicos usam nomes semânticos; não houve alteração de chunking, embeddings, PGVector ou contrato HTTP.
- Pendência: imports externos dos nomes antigos deixam de funcionar e devem ser migrados.
- Verificação: testes, evaluation, compilação, busca de referências antigas e hook estrutural previstos nesta rodada.

## v1 — Renomeação verificada

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificação: 36 testes, evaluation `20/20`, compilação, imports novos, busca sem referências ativas antigas e `git diff --check` aprovados.
- Pendências: consumidores externos dos nomes antigos precisam migrar; smoke externo não foi repetido nesta rodada.

## v2 — Nomenclatura semântica aplicada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Mudanças: persistência virou `persist_document_chunks`; busca virou `search_relevant_chunks`; containers, use cases, stores e adapter receberam nomes explícitos; fluxo completo virou `extract_chunk_and_persist_document`.
- Problema resolvido: separar semanticamente persistência, busca e adaptação LangChain nos nomes do runtime.
- Verificação: testes, evaluation, compilação, referências antigas e hook estrutural previstos nesta rodada.
- Pendência: finalizar a implementação após a verificação.
