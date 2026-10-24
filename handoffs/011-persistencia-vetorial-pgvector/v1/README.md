# 011 v1 — Backend vetorial PostgreSQL

- Versão-base: estado real após `008`; `009` e `010` conferidas como propostas e deixadas em standby.
- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Arquivos reais: `docker-compose.yml`, `infra/postgres/init/001-vector-schema.sql`, `rastro-ai/pyproject.toml`, módulos Python de portas, embeddings, retrieval, README e testes.
- Operação: insert de serviço, volume, schema, adapter, provider e testes; replace da seleção do store e documentação.

## O que foi feito

Foi criado PostgreSQL `pgvector/pgvector:pg16` com volume `rastro_vector_db` e schema compatível com Supabase. A IA gera embeddings multilíngues de 384 dimensões, grava chunks com offsets e consulta por distância cosine quando `VECTOR_STORE_BACKEND=postgres`; o backend em memória foi preservado.

## O que muda na aplicação

Com `postgres`, indexação e retrieval passam a ser persistentes e semânticos, com isolamento por projeto e upsert idempotente. O padrão continua `memory`; o upload da API ainda não dispara a pipeline, o modelo é baixado na primeira utilização e o stack completo do Supabase não é iniciado.

## Jornada da aplicação nesta versão

Antes, chunks eram ranqueados lexicalmente em memória e desapareciam ao reiniciar. Agora, a aplicação pode persistir chunks e consultar significado semântico no PostgreSQL/pgvector, mantendo citações e offsets. A próxima evolução é ligar o upload ao processamento.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose up -d vector-db` na raiz.
2. Defina `DATABASE_URL=postgresql://rastro:rastro@localhost:5432/rastro` e `VECTOR_STORE_BACKEND=postgres`.
3. Instale as dependências com `pip install -e rastro-ai`.
4. Use `index_document`, `index_chunks` e `retrieve_chunks`/`answer_question` das fachadas Python.
5. Resultado esperado: `document_chunks` contém os chunks e retrieval retorna resultados semânticos filtrados por `project_id`.

## Cobertura por comportamento

- Persistência/upsert e dimensão: `rastro-ai/tests/test_postgres_vector_store.py`; esperado: SQL com upsert e rejeição de dimensão inválida.
- Consulta semântica e isolamento: teste unitário do adapter; esperado: score, offsets, documento e projeto preservados.
- Schema real: container saudável, extensão `vector`, tabela e índices confirmados.
- Integração real: adapter executado contra o PostgreSQL do Compose; smoke de upsert, consulta e isolamento por projeto aprovado.
- Regressão: suíte Python completa; esperado: todos os testes aprovados.

## Instruções de validação

- `python3 -m compileall -q src tests` em `rastro-ai/`; esperado: código 0 e saída vazia.
- `python3 -m unittest discover -s tests -v` em `rastro-ai/`; esperado: 21 testes aprovados.
- `docker compose config`; esperado: configuração válida com `vector-db`, volume, schema montado e porta publicada por `VECTOR_DB_PORT` (padrão `55432`).
- `python3 -m unittest discover -s tests -v` executado em `rastro-ai/`; resultado: 21 testes aprovados.
- `python3 -m compileall -q src tests` executado em `rastro-ai/`; resultado: compilação aprovada.
- `docker compose config` executado na raiz; resultado: configuração válida.
- `docker compose up -d vector-db`; esperado: PostgreSQL saudável em `localhost:55432` (ou na porta definida por `VECTOR_DB_PORT`).
- `docker compose exec vector-db psql -U rastro -d rastro -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"`; esperado: uma linha `vector`.
- `docker compose exec vector-db psql -U rastro -d rastro -c "\\d document_chunks"`; esperado: tabela com `embedding vector(384)` e chave composta.
- Com `DATABASE_URL=postgresql://rastro:rastro@localhost:55432/rastro VECTOR_STORE_BACKEND=postgres`, executar o fluxo Python; esperado: upsert e retrieval persistentes sem cruzar projetos.
- Resultado real: adapter PostgreSQL executado contra o container, com upsert, busca e isolamento por projeto aprovados.
