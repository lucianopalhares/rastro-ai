# 017 — Renomear fluxo de extração e chunking
- Data/hora: 2026-10-25 -03:00 | Status: `verified`; aplicação: IA (`rastro-ai`).
- Objetivo: substituir nomes ambíguos de indexação por nomes que expressem extração, chunking e persistência.
- Dependência/ordem: `016` verificada; renomeação aplicada no serviço Python, testes, exports e documentação.
- Impacto: `extract_and_chunk_document()` gera chunks; `extract_chunk_and_persist_document()` também gera embeddings e persiste no PGVector.
- Evolução: `v1` separou extração de persistência; `v2` esclareceu métodos, containers, casos de uso, stores e adapters sem alterar o runtime.
- Pendências: consumidores externos dos nomes antigos precisam migrar; comportamento funcional permanece preservado.
- Pasta: `handoffs/017-renomear-fluxo-extracao-chunking/`; próxima ação: verificar e finalizar `017`.
