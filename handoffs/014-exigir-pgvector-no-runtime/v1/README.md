# 014/v1 — Plano para exigir pgvector no runtime

- Versão: `v1`; versão-base: implementação `013` verificada; data: 2026-10-25 -03:00; status: `proposed`.
- Aplicação: serviço Python `rastro-ai`; nesta rodada não há alteração de runtime.
- Arquivos reais a conferir: `rastro-ai/src/rastro_ai/retrieval.py`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/in_memory_vector_store.py`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py`, `rastro-ai/tests/test_retrieval.py`, `rastro-ai/tests/test_postgres_vector_store.py`, `rastro-ai/README.md`, `docker-compose.yml` e `infra/postgres/init/001-vector-schema.sql`.
- Estado inicial: `PostgresVectorStore` e embeddings já existem; `InMemoryVectorStore` continua selecionado quando `VECTOR_STORE_BACKEND` está ausente; a configuração Docker usa PostgreSQL.

## O que foi feito

- Criado o registro da tarefa para corrigir a divergência entre o comportamento declarado de busca semântica e o fallback lexical em memória.
- Definido o critério de aplicação: indexação e busca devem passar pelo backend persistente com embeddings, e configuração ausente ou inválida deve falhar explicitamente.
- Nenhum arquivo de aplicação foi alterado nesta rodada; a próxima rodada deverá reler as âncoras e aplicar somente a diferença necessária.

## O que muda na aplicação

- Planejado: o runtime Python não deverá trocar silenciosamente para `InMemoryVectorStore`; o caminho oficial será `PostgresVectorStore` com pgvector.
- O adaptador em memória poderá permanecer apenas para testes explícitos, desde que não seja usado como fallback de produção e tenha nome/documentação coerentes com seu comportamento lexical.
- Fora do escopo: troca de banco, deploy, migração externa, mudança do modelo de embeddings, retry e processamento assíncrono.
- Risco: testes locais ou ambientes sem PostgreSQL precisarão declarar uma estratégia de teste explícita; custo e latência de embeddings devem continuar documentados.

## Jornada da aplicação nesta versão

Antes, uma execução sem configuração podia indexar e consultar usando contagem de palavras, embora o fluxo de produção fosse baseado em embeddings. A tarefa prepara a correção para que o comportamento semântico seja único e verificável, com erro claro quando o backend persistente não estiver disponível. O resultado esperado é consistência entre desenvolvimento integrado, produção e avaliação; testes unitários isolados poderão continuar usando doubles explícitos.

## Como usar e validar a aplicação nesta versão

Esta versão ainda não altera o runtime. Na aplicação da próxima rodada, o uso esperado será subir `vector-db` e `ai-indexer` com `VECTOR_STORE_BACKEND=postgres`, enviar um documento pelo endpoint de upload e consultar os chunks persistidos no PostgreSQL/pgvector. Ambientes sem banco deverão produzir erro de configuração, não uma busca lexical silenciosa.

## Cobertura por comportamento

- Seleção de backend: teste unitário/contratual deverá provar que `postgres` é obrigatório e que configuração ausente ou inválida falha explicitamente.
- Indexação: teste do `PostgresVectorStore` deverá confirmar geração/persistência dos embeddings e upsert por projeto/documento/chunk.
- Busca: teste deverá confirmar embedding da consulta, similaridade cosine e filtro por `project_id`.
- Integração real: smoke com Compose e PostgreSQL/pgvector será necessário na aplicação; não foi executado nesta rodada.

## Instruções de validação

- `git status --short`: esperado, somente os handoffs da implementação proposta aparecem como novos/alterados nesta rodada.
- `sed -n '1,220p' handoffs/014-exigir-pgvector-no-runtime/v1/README.md`: esperado, plano, escopo, jornada, cobertura e critérios de validação estão registrados.
- Na próxima rodada, executar a suíte Python, `python -m compileall rastro-ai/src`, `docker compose config`, smoke HTTP do upload e `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com os quatro arquivos da implementação.
