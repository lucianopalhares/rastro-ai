## v1 — Tarefa proposta

- Data/hora: 2026-10-25 -03:00.
- Status: `proposed`.
- Aplicação: serviço Python `rastro-ai`; dependência: implementação `014` verificada.
- Plano: conectar o `TextChunker` ao `IndexDocumentUseCase`, criar adaptador de infraestrutura com `langchain-text-splitters` e converter a saída para `DocumentChunk`.
- Invariantes: normalização, offsets, índice, `project_id`, sobreposição, limites de tokens e compatibilidade dos embeddings devem permanecer cobertos.
- Pendências: confirmar API/versão da biblioteca, estratégia de offsets e impacto no baseline antes de alterar o runtime.
- Verificação prevista: dependências, testes de chunking/indexação, evaluation baseline, compilação, smoke de upload e hook estrutural.

## v2 — Adaptador aplicado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `pyproject.toml`, porta `TextChunker`, caso de uso, fachada `indexing.py`, adaptador LangChain e `tests/test_indexing.py`.
- Mudanças: dependência declarada, chunker injetado, `RecursiveCharacterTextSplitter` isolado na infraestrutura e conversão para `DocumentChunk` com offsets defensivos.
- Problema resolvido: remove o acoplamento direto do caso de uso ao serviço concreto de domínio.
- Verificação: 30 testes, evaluation 20/20, `compileall`, build sem cache, import no container, serviço saudável via Compose e hook aprovados.
- Pendências: medir custo/latência e executar smoke API → Python → pgvector em rodada de finalização.

## v3 — Dependência adicionada às imagens

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `rastro-ai/Dockerfile` e `rastro-ai/Dockerfile.dev`.
- Mudança: os comandos de instalação passaram a incluir `langchain-text-splitters>=0.3,<1` junto das dependências existentes.
- Problema resolvido: o container `ai-indexer` encerrava durante o import com `ModuleNotFoundError` porque a imagem não instalava a dependência declarada no `pyproject.toml`.
- Verificação: build sem cache, import no container, serviço saudável via Compose, testes Python/evaluation, compilação e hook estrutural aprovados.

## v4 — Fachada pública unificada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `rastro-ai/src/rastro_ai/indexing.py` e `rastro-ai/tests/test_indexing.py`.
- Mudança: `rastro_ai.indexing.chunk_text` passou a delegar ao mesmo `LangChainTextChunker` usado por `IndexDocumentUseCase`.
- Problema resolvido: chamadas públicas diretas e indexação de arquivos podiam usar estratégias diferentes de chunking.
- Verificação: 31 testes, evaluation `20/20` e compilação aprovados; hook estrutural executado após o registro.
- Pendências: manter o serviço de domínio antigo apenas até confirmar que consumidores internos não dependem dele; commit aguarda finalização.

## v5 — Embeddings adaptados ao LangChain

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: repository de embeddings OpenAI, `pyproject.toml`, `Dockerfile`, `Dockerfile.dev` e teste do repository.
- Mudança: `OpenAIEmbeddingRepository` passou a delegar batching e transporte a `langchain_openai.OpenAIEmbeddings`, mantendo a porta local e validação de dimensão.
- Problema resolvido: integra o padrão de embeddings do ecossistema LangChain sem acoplar os casos de uso ou substituir o store pgvector próprio.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, import no container e hook aprovados; chamada OpenAI real não executada sem credencial.
- Pendências: medir custo/latência e validar smoke com credencial em finalização; commit aguarda solicitação explícita.

## v6 — Vector store LangChain aplicado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: repository pgvector, testes do store, `pyproject.toml`, `Dockerfile` e `Dockerfile.dev`.
- Mudança: `PostgresVectorStore` passou a adaptar `langchain-postgres`/`PGVector`, mantendo `VectorStore`, metadata, IDs determinísticos, filtro por projeto e conversão de scores.
- Problema resolvido: integra o vector store padrão do ecossistema LangChain sem expor `Document` aos casos de uso.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, upsert/busca reais do PGVector no PostgreSQL e hook aprovados.
- Pendências: reindexar dados existentes na coleção LangChain, executar smoke com OpenAI e medir custo/latência; commit aguarda finalização.

## v7 — Preparação do pipeline RAG

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: portas e casos de uso de aplicação, adapters de reranking/generation, prompt, workflow LangGraph, testes, `pyproject.toml` e Dockerfiles.
- Mudança: adicionados contratos para reranking e geração, adapters LangChain com citações estruturadas, prompt reutilizável e grafo opcional de retrieval → reranking → resposta.
- Problema resolvido: prepara a evolução para RAG generativo sem acoplar casos de uso ao modelo, prompt ou orquestrador.
- Verificação: 35 testes, evaluation `20/20`, compilação, build Docker, import do workflow no container e hook aprovados.
- Pendências: escolher reranker/modelo, configurar credenciais, ativar o grafo no runtime e medir qualidade/custo/latência.

## v8 — Comentário explicativo do splitter

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivo real: `rastro-ai/src/rastro_ai/document_indexing/infrastructure/chunking/langchain_text_chunker.py`.
- Mudança: adicionada uma explicação simples acima de `RecursiveCharacterTextSplitter`.
- Comportamento: nenhuma alteração de runtime; a documentação inline explica que o texto é dividido em partes menores.
- Verificação: testes existentes permanecem aplicáveis; hook estrutural executado após o registro.

## v9 — Remoção do schema vetorial legado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `infra/postgres/init/001-vector-schema.sql` e runtime `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py` conferidos.
- Mudança: o init mantém somente a extensão `vector`; a tabela antiga `document_chunks` deixou de ser criada, pois o runtime atual usa `langchain_pg_collection` e `langchain_pg_embedding` via `PGVector`.
- Problema resolvido: elimina a ambiguidade entre o schema próprio anterior e as tabelas efetivamente usadas pela indexação atual.
- Verificação: referências de runtime conferidas; remoção da tabela local executada; coleção LangChain e embeddings preservados; hook estrutural pendente nesta rodada.
- Pendências: bases existentes precisam aplicar a remoção explicitamente; não há migração dos 27 registros legados nesta rodada.

## 015 — Finalização verificada

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Arquivos e controles: versões `v1` a `v9`, código Python, schema pgvector, documentação arquitetural, README, `.gitignore`, Compose e banco local conferidos.
- Verificações: coleção LangChain preservada, tabela legada removida, compilação/hook e consultas PostgreSQL executados; pytest não disponível na imagem do indexador.
- Pendências: dados legados removidos não foram migrados; não há próxima etapa ativa na sequência.
- Commit: será registrado após a criação do commit explícito desta implementação.

## 015 — Commit criado

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Commit: `607a22c` — `Consolidar fluxo LangChain de indexação`.
- Verificação: commit criado com lista explícita de 48 arquivos da implementação; alterações não relacionadas permaneceram fora do índice.
