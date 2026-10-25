# Linha do tempo — 012/v5 Timeout da chamada de embeddings

## v5 — Ajuste aplicado

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Arquivos reais conferidos: `docker-compose.yml`, gateway HTTP da API e logs do `ai-indexer`.
- Mudança aplicada: `AI_INDEXING_TIMEOUT_MS=60000` no serviço API do Compose.
- Problema resolvido: timeout de 10 segundos fechava a conexão durante embedding externo de documento longo.
- Verificação: upload longo retornou `ready`; consulta confirmou 3 chunks, conteúdo não vazio, embeddings presentes e dimensão `384`.
- Pendência: nenhuma nesta versão; evaluation semântica permanece evolução futura.
