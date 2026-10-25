# 014/v2 — Exigir pgvector no runtime

- Versão: `v2`; versão-base: `v1` proposta; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai`; a rodada foi reconciliada com o código real antes da alteração.
- Estado encontrado: `retrieval.py` selecionava memória quando `VECTOR_STORE_BACKEND` estava ausente ou diferente de `postgres`; Docker já configurava PostgreSQL; testes e evaluation importavam o store lexical explicitamente.
- Arquivos alterados: `rastro-ai/src/rastro_ai/retrieval.py`, `rastro-ai/src/rastro_ai/service.py`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/in_memory_vector_store.py`, `rastro-ai/tests/test_indexing.py`, `rastro-ai/tests/test_runtime_vector_store.py` e `rastro-ai/README.md`.

## O que foi feito

- Substituída a seleção implícita por validação explícita de `VECTOR_STORE_BACKEND=postgres`; ausência ou valor `memory` agora falha durante a construção do runtime.
- Removido o import do adaptador em memória da fachada de runtime; o store lexical foi documentado como double de testes/evaluation, sem remoção dos usos explícitos existentes.
- Atualizada a resposta do endpoint para reportar `postgres` como backend esperado e a documentação da IA para distinguir runtime semântico de evaluation lexical.
- Adicionados testes de subprocesso para provar que o runtime rejeita configuração ausente ou lexical; o teste de indexação foi ajustado para declarar configuração PostgreSQL ao importar a fachada.

## O que muda na aplicação

- O serviço Python deixa de funcionar como busca lexical quando o backend não está configurado: indexação e consulta exigem o caminho `PostgresVectorStore` com embeddings.
- Testes unitários e evaluation determinística continuam usando `InMemoryVectorStore` somente por dependência explícita, fora da seleção de runtime.
- O Docker Compose permanece compatível e já fornece `VECTOR_STORE_BACKEND=postgres`, `DATABASE_URL`, `OPENAI_API_KEY`, modelo e dimensão `384`.
- Limites: a rodada não troca o modelo, não altera o schema, não executa deploy/migração externa e ainda requer dependências Python instaladas para a suíte completa.
- Impacto de IA: elimina divergência de qualidade entre ambientes; não altera modelo, prompt, custo ou latência do caminho PostgreSQL, mas torna obrigatória a chamada de embeddings no runtime.

## Jornada da aplicação nesta versão

Antes, o upload podia cair em um índice lexical em memória quando a configuração estava ausente, ocultando uma execução sem embeddings. Agora, o serviço só inicia a fachada de retrieval com backend persistente explicitamente configurado; o fluxo Docker continua enviando chunks para OpenAI e pgvector, enquanto testes determinísticos escolhem o double diretamente. A pessoa operadora recebe erro de configuração em vez de uma falsa confirmação semântica.

## Como usar e validar a aplicação nesta versão

1. Defina `OPENAI_API_KEY` no `.env` da raiz.
2. Suba `docker compose up -d vector-db ai-indexer api`; o Compose fornece `VECTOR_STORE_BACKEND=postgres` e a URL interna do PostgreSQL.
3. Execute o upload documentado em `README.md` ou `rastro-api/README.md`; espere documento `ready` quando a chave for válida.
4. Para validar a falha explícita, execute `PYTHONPATH=rastro-ai/src env -u VECTOR_STORE_BACKEND python3 -c 'import rastro_ai.retrieval'`; espere `ValueError: VECTOR_STORE_BACKEND must be 'postgres'`.

## Cobertura por comportamento

- Seleção de backend: `rastro-ai/tests/test_runtime_vector_store.py` cobre ausência e `memory`; ambos falham com mensagem explícita.
- Indexação e busca PostgreSQL: `rastro-ai/tests/test_postgres_vector_store.py` cobre upsert, embedding, dimensão, filtro por projeto e consulta cosine com fake de infraestrutura.
- Retrieval isolado: `rastro-ai/tests/test_retrieval.py` e `rastro-ai/tests/test_answers.py` preservam o uso explícito do double lexical.
- Integração real: `docker compose config` foi validado; smoke HTTP e banco real dependem de `OPENAI_API_KEY`, ausente neste ambiente.

## Instruções de validação

- `uv run --project . --with tiktoken --with 'psycopg[binary]' python -m unittest discover -s tests -p 'test_*.py'`: executado, 28 testes aprovados.
- `python3 -m unittest tests.test_runtime_vector_store tests.test_postgres_vector_store tests.test_retrieval tests.test_answers`: esperado, 12 testes direcionados aprovados no ambiente com dependências instaladas.
- `python3 -m compileall -q rastro-ai/src`: esperado, compilação sem erros.
- `docker compose config`: esperado, `VECTOR_STORE_BACKEND=postgres`, `DATABASE_URL` para `vector-db`, `EMBEDDING_MODEL=text-embedding-3-small` e `EMBEDDING_DIMENSIONS=384` presentes.
- `PYTHONPATH=rastro-ai/src env -u VECTOR_STORE_BACKEND python3 -c 'import rastro_ai.retrieval'`: esperado, falha com `ValueError: VECTOR_STORE_BACKEND must be 'postgres'`.
- `docker compose ps --status running`: executado, `vector-db`, `ai-indexer` e `api` saudáveis; upload HTTP real não executado porque `OPENAI_API_KEY` não está disponível.
- `docker compose up -d vector-db ai-indexer api` e upload HTTP documentado: esperado, indexação usa PostgreSQL/pgvector e retorna `backend: postgres`; requer `OPENAI_API_KEY` válida.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/014-exigir-pgvector-no-runtime/README.md handoffs/014-exigir-pgvector-no-runtime/TIMELINE.md handoffs/014-exigir-pgvector-no-runtime/v2/README.md handoffs/014-exigir-pgvector-no-runtime/v2/TIMELINE.md`: esperado, quatro arquivos válidos.
