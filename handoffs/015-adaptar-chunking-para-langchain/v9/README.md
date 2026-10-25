# 015/v9 — Remoção do schema vetorial legado

- Versão: `v9`; versão-base: `v8`; data: 2026-10-25 -03:00; status: `applied`.
- Versão-base comparada: `v8`; o runtime já usava `PGVector`, mas o init ainda criava `document_chunks`.
- Arquivos conferidos: `infra/postgres/init/001-vector-schema.sql`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py`, `docker-compose.yml`, `docs/architecture/document-upload-indexing-flow.md`, `README.md`, `.gitignore` e tabelas reais do PostgreSQL.
- Operação: removida a criação da tabela antiga; removida a tabela existente no banco local; preservada somente a extensão `vector` e as tabelas do LangChain.
- Impacto: novos ambientes não criam `document_chunks`; registros antigos dessa tabela não foram migrados e não são mais usados pelo runtime.
- Próxima ação: solicitar finalização da implementação 015 após revisar a decisão sobre os dados legados.

## O que foi feito

- O schema inicial deixou de criar `document_chunks`, porque a persistência atual chama `PGVector.add_embeddings()` e grava em `langchain_pg_collection` e `langchain_pg_embedding`.
- A tabela local antiga foi removida após a conferência de que não existem referências de runtime a ela.
- Nenhuma tabela ou dado da coleção usada pelo LangChain foi removido.

## O que muda na aplicação

- O runtime permanece igual: chunks novos continuam sendo gravados pelo `langchain-postgres`.
- Em bancos novos, somente a extensão `vector` será preparada pelo script inicial; o `PGVector` criará suas tabelas ao iniciar.
- A remoção da tabela antiga é destrutiva para os 27 registros legados existentes neste banco local; eles não foram migrados nesta rodada.
- Não houve alteração em chunking, embeddings, dimensão 384, coleção `rastro_document_chunks` ou isolamento por projeto.

## Jornada da aplicação nesta versão

Antes, o banco mantinha a tabela antiga `document_chunks` ao lado das tabelas do LangChain. Agora, o schema inicial prepara somente a extensão `vector`, a tabela antiga foi removida do banco local e a indexação continua usando a coleção do `PGVector`.

## Como usar e validar a aplicação nesta versão

Reinicie a base local somente se precisar testar um banco novo; em bases existentes, a remoção já foi aplicada manualmente nesta rodada. O fluxo continua sendo exercitado pelo upload:

```bash
curl --fail-with-body --request POST \
  --url http://127.0.0.1:3039/api/v1/documents/upload \
  --header 'accept: application/json' \
  --form 'projectId=debug-project' \
  --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"
```

Execute também as consultas da seção de validação para confirmar a ausência da tabela antiga e a preservação da coleção LangChain.

## Cobertura por comportamento

- Persistência vetorial: a tabela antiga não existe e `langchain_pg_embedding` mantém os quatro embeddings existentes.
- Infraestrutura: a extensão `vector` permanece instalada para o `PGVector`.
- Regressão: o runtime não possui referência à tabela antiga; o nome da coleção LangChain permanece configurável.
- Evidência de teste de contrato: `rastro-ai/tests/test_postgres_vector_store.py` cobre a chamada ao adapter `PGVector` e a preservação de metadata, IDs e dimensão dos vetores.
- Validação integrada/manual: a consulta ao PostgreSQL confirmou a remoção da tabela antiga e a preservação dos embeddings existentes.

## Instruções de validação

- `rg -n "document_chunks\\b" infra/postgres/init/001-vector-schema.sql rastro-ai/src rastro-api/src`: esperado, nenhuma referência de runtime ou criação da tabela antiga.
- `docker compose exec -T vector-db psql -U rastro -d rastro -c "SELECT to_regclass('public.document_chunks') AS legacy_table, to_regclass('public.langchain_pg_collection') AS collection_table, to_regclass('public.langchain_pg_embedding') AS embedding_table;"`: esperado, `legacy_table` nulo e as duas tabelas LangChain presentes.
- `docker compose exec -T vector-db psql -U rastro -d rastro -c "SELECT count(*) FROM langchain_pg_embedding;"`: esperado, os embeddings existentes permanecem acessíveis.
- `docker compose exec -T vector-db psql -U rastro -d rastro -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"`: esperado, a extensão `vector` continua instalada.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v9/README.md handoffs/015-adaptar-chunking-para-langchain/v9/TIMELINE.md`: esperado, handoffs válidos.
