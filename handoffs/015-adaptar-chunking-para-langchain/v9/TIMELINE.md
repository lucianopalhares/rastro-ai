## v9 — Remoção do schema vetorial legado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `infra/postgres/init/001-vector-schema.sql`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py` e tabelas do PostgreSQL.
- Mudanças: removida a criação e a tabela local `document_chunks`; preservadas a extensão `vector`, `langchain_pg_collection` e `langchain_pg_embedding`.
- Problema resolvido: elimina a confusão entre o schema antigo e o armazenamento efetivamente usado pelo PGVector.
- Pendências: os 27 registros legados não foram migrados; a remoção precisa ser aplicada separadamente em outros bancos existentes.
- Verificação: referências e contagens conferidas; hook estrutural será executado após o registro.

## v9 — Verificação final

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Verificação: `document_chunks` não existe; `langchain_pg_collection`, `langchain_pg_embedding` e a extensão `vector` permanecem disponíveis; quatro embeddings foram preservados.
- Hook: `validate-handoffs.sh` executado com sucesso após a inclusão da cobertura comportamental.
