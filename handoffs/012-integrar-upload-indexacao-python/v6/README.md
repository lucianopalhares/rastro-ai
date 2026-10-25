# 012/v6 — Separação modular da aplicação Python

- Versão-base: `v5` aplicada; estrutura real reconciliada em 2026-10-25.
- Status: `applied`; aplicação: `rastro-ai`.
- Estado encontrado: `document_indexing` concentrava ingestão, chunking, embeddings e busca semântica em um único namespace.
- Decisão: criar limites `documents`, `chunking`, `embeddings`, `semantic_search` e `document_ingestion`; manter o namespace antigo como compatibilidade.

## O que foi feito

Foram criados pontos de importação separados por capacidade e as fachadas de produção foram direcionadas para eles. Chunking, embeddings, busca semântica e ingestão agora têm módulos próprios; adapters antigos continuam disponíveis para não quebrar consumidores externos.

## O que muda na aplicação

O comportamento funcional permanece igual: o upload continua indexando, gerando embeddings e persistindo chunks. A mudança é estrutural e reduz acoplamento; `document_indexing` ainda existe como camada de compatibilidade e poderá ser removido somente após migração dos consumidores.

## Jornada da aplicação nesta versão

Antes, localizar ou substituir uma capacidade exigia navegar por um módulo agregado. Agora, a ingestão depende do chunking, embeddings e busca semântica por limites explícitos, facilitando trocar OpenAI, pgvector ou a política de chunks sem misturar responsabilidades.

## Como usar e validar a aplicação nesta versão

Use os imports novos, por exemplo `from rastro_ai.chunking.domain.chunker import chunk_text`, `from rastro_ai.embeddings.infrastructure.openai.repository import OpenAIEmbeddingRepository` e `from rastro_ai.semantic_search.infrastructure.pgvector.repository import PostgresVectorStore`. Os imports antigos continuam funcionando durante a transição.

## Cobertura por comportamento

- Limites modulares: evidência contratual de import smoke confirma os novos módulos de documentos, ingestão, chunking, embeddings e busca semântica.
- Compatibilidade: evidência unitária dos 26 testes Python existentes continua aprovada usando o namespace antigo.
- Integração/smoke: repetida após a reorganização; documento curto retornou `ready` com 1 chunk e documento longo `ready` com 3 chunks, todos com embeddings `384` persistidos.

## Instruções de validação

- `PYTHONPATH=src /tmp/rastro-ai-venv/bin/python -c "from rastro_ai.chunking.domain.chunker import chunk_text; from rastro_ai.document_ingestion.application.use_cases import IndexDocumentUseCase; from rastro_ai.embeddings.infrastructure.openai.repository import OpenAIEmbeddingRepository; from rastro_ai.semantic_search.infrastructure.pgvector.repository import PostgresVectorStore; print('modular-imports-ok')"`: esperado, `modular-imports-ok`.
- `cd rastro-ai && /tmp/rastro-ai-venv/bin/python -m unittest discover -s tests -v`: esperado, 26 testes aprovados.
- `docker compose build ai-indexer`: esperado, imagem construída com a estrutura modular.
- Upload real curto e longo pela API: confirmado, estados `ready`, chunks persistidos, conteúdo não vazio e embeddings presentes com dimensão `384` no PostgreSQL.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v2/README.md handoffs/012-integrar-upload-indexacao-python/v2/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v3/README.md handoffs/012-integrar-upload-indexacao-python/v3/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v4/README.md handoffs/012-integrar-upload-indexacao-python/v4/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v5/README.md handoffs/012-integrar-upload-indexacao-python/v5/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v6/README.md handoffs/012-integrar-upload-indexacao-python/v6/TIMELINE.md`: esperado, 14 arquivos válidos.
