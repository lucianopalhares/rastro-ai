# Linha do tempo — 012/v2 Modelo Document e embeddings externos

## v2 — Repository externo aplicado

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: contrato/gateway API, serviço Python, ports, retrieval, store PostgreSQL, schema, Compose, Dockerfile e testes.
- Mudanças aplicadas: API envia `Document.toJSON()`, `EmbeddingRepository` em lote, `OpenAIEmbeddingRepository`, dimensão `384`, configuração PostgreSQL e porta externa `18473`.
- Problema resolvido: integração deixou de reconstruir DTO paralelo e passou a separar contrato de embeddings do fornecedor.
- Verificação: 10 testes API, 24 testes Python, build da imagem sem CUDA, Compose config e diff check aprovados.
- Pendência: chamada real OpenAI e confirmação de linha no banco aguardam `OPENAI_API_KEY`, ausente nesta sessão.
