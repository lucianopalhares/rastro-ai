## v1 — Composition root aplicado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai`; versão-base: `015` verificada; arquivos reais conferidos antes da alteração.
- Mudanças: criado `src/rastro_ai/bootstrap/container.py`; fachadas `indexing.py` e `retrieval.py` passaram a construir dependências explicitamente; testes de runtime foram ajustados.
- Problema resolvido: `retrieval.py` criava vector store durante o import e as fachadas mantinham instâncias globais fora de um composition root.
- Impacto: importação de `rastro_ai.retrieval` tornou-se segura; a exigência de `VECTOR_STORE_BACKEND=postgres` permanece na construção do container.
- Verificação: testes unitários, evaluation, compilação e hook estrutural previstos nesta rodada; nenhuma alteração externa ou migração executada.
- Pendências: consolidar aliases de namespace, mover workflows para `orchestration` e separar runners de evaluation.

## v1 — Composition root verificado

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificações: 36 testes aprovados, evaluation `20/20`, importação sem `VECTOR_STORE_BACKEND`, compilação, `git diff --check` e hook estrutural aprovados.
- Evidência: o runtime continua rejeitando backend ausente ou lexical somente na construção do container, enquanto a importação da fachada termina com `import ok`.
- Pendências: namespaces duplicados, workflows e evaluation continuam planejados para `017`, `018` e `019`.
- Commit: aguardando o comando explícito de finalização da implementação `016`.

## v2 — Duplicações removidas

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Arquivos reais conferidos: imports do runtime, testes, evaluation, entrypoints Docker e todos os módulos Python sob `src/rastro_ai`.
- Mudanças: removidos os namespaces duplicados `chunking`, `document_ingestion`, `documents`, `embeddings` e `semantic_search`, além de `SentenceTransformerEmbeddingProvider`; imports internos foram apontados para `document_indexing`.
- Problema resolvido: aliases sem consumidores internos e provider sem dependência declarada aumentavam a superfície e mantinham caminhos de chunking diferentes.
- Verificação: 36 testes, evaluation `20/20`, compilação e busca de referências residuais aprovados.
- Pendência: imports externos dos aliases antigos não são mais compatíveis e devem migrar para as fachadas públicas ou o namespace canônico.

## 016 — Finalização

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificações finais: testes, evaluation, compilação, imports canônicos, rejeição dos aliases removidos, hook estrutural e `git diff --check` aprovados.
- Arquivos: aplicação Python, testes, documentação e handoffs `016/v1` e `016/v2` conferidos; implementações anteriores preservadas.
- Pendências: consumidores externos dos aliases removidos não foram pesquisados fora do repositório; sem deploy ou migração.
- Próxima etapa: `017-consolidar-namespaces-python`; `CURRENT.md` avançado para `017`.
- Commit: `ceb639e` — `Reorganizar arquitetura do serviço Python`.
- Verificação do commit: lista explícita de 50 arquivos da implementação; alterações não relacionadas ficaram fora do índice.
