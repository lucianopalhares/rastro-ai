## v3 — Verificação real do fluxo persistente

- Data/hora: 2026-10-25 10:18 -03:00.
- Status: `verified`.
- Arquivos reais conferidos: API de upload, serviço Python, Compose, schema e tabela PostgreSQL/pgvector.
- Verificação aplicada: upload real retornou `status: ready`; banco confirmou 1 chunk com embedding de dimensão `384`; `POST /index` direto retornou `backend: postgres`.
- Problema resolvido: confirmação externa pendente sobre o uso real de embeddings e pgvector.
- Testes: 28 testes Python, compilação, Compose, containers saudáveis e hook estrutural aprovados.
- Pendências: nenhuma dentro do escopo da implementação; retry e processamento assíncrono permanecem fora do escopo.
