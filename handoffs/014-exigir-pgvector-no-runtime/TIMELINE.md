## v1 — Tarefa proposta

- Data/hora: 2026-10-25 -03:00.
- Status: `proposed`.
- Arquivos reais a conferir: `rastro-ai/src/rastro_ai/retrieval.py`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/in_memory_vector_store.py`, `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py`, testes, README da IA, Compose e schema pgvector.
- Mudança planejada: remover a seleção implícita do backend lexical e exigir configuração persistente com embeddings e pgvector; manter doubles de teste somente onde forem necessários.
- Problema: execução sem `VECTOR_STORE_BACKEND=postgres` usa `InMemoryVectorStore`, que não gera embeddings e não representa a busca semântica de produção.
- Pendências: reconciliar as âncoras com o código real, decidir o destino do adaptador em memória e implementar testes/documentação.
- Verificação prevista: suíte Python, `compileall`, Compose/configuração, smoke HTTP com PostgreSQL/pgvector e hook estrutural.

## v2 — Aplicação do backend persistente obrigatório

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Arquivos reais conferidos: fachada de retrieval, handler HTTP, adaptadores, testes, README da IA, Compose e schema pgvector.
- Mudanças aplicadas: backend ausente ou lexical agora falha; memória ficou restrita a uso explícito; documentação e testes foram atualizados.
- Problema resolvido: runtime não degrada silenciosamente para ranking lexical sem embeddings.
- Verificação: 28 testes, `compileall`, `docker compose config`, containers saudáveis e hook estrutural passaram; import sem backend falhou explicitamente como esperado.
- Pendências: smoke HTTP com PostgreSQL/OpenAI e promoção para `verified`.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/`.

## Finalização — aplicação confirmada, verificação externa pendente

- Data/hora: 2026-10-25 -03:00 | Status mantido: `applied`.
- Verificações finais: 28 testes Python, compilação, `docker compose config`, três containers saudáveis e hook estrito aprovados.
- Pendência impeditiva: smoke HTTP real com embeddings OpenAI não foi executado porque `OPENAI_API_KEY` não está disponível neste ambiente.
- Commit: não gerado; a política exige resolver a pendência de verificação antes do commit automático.
- Controle: `CURRENT.md` permanece em `014`; próxima ação é executar o smoke com chave válida e então promover para `verified`.

## v3 — Verificação real do fluxo persistente

- Data/hora: 2026-10-25 10:18 -03:00 | Status: `verified`.
- Verificação: upload API retornou `ready`; banco confirmou 1 chunk com embedding `384`; `POST /index` direto retornou `backend: postgres`.
- Testes: 28 testes Python, compilação, Compose, containers saudáveis e hook estrutural aprovados.
- Pendências: nenhuma dentro do escopo; retry e processamento assíncrono continuam fora do escopo.
- Commit: autorizado pela evidência completa; lista explícita será conferida antes da criação.

## Commit da implementação

- Commit: `52e1820` — `Exigir pgvector no runtime`.
- Arquivos: código Python, teste de configuração, README da IA e handoffs/controlos explícitos da tarefa `014`.
- Verificação: smoke API/Python/pgvector, 28 testes, compilação, Compose e hook estrutural aprovados antes do commit.
