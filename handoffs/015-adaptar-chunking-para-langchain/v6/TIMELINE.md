## v6 — Vector store LangChain aplicado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai` e PostgreSQL/pgvector.
- Mudança: `PostgresVectorStore` passou a adaptar `langchain-postgres.PGVector` com ponte de embeddings, metadata e IDs determinísticos.
- Compatibilidade: porta `VectorStore`, `DocumentChunk`, offsets, projeto, dimensão e score local preservados.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, upsert/busca reais do PGVector no Compose e hook aprovados.
- Pendências: reindexar dados da tabela antiga e executar smoke com OpenAI; commit aguarda finalização.
