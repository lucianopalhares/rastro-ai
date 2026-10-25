## v4 — Fachada pública unificada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai`.
- Mudança: `indexing.chunk_text` passou a usar `LangChainTextChunker`, igual ao caso de uso de indexação.
- Problema resolvido: elimina estratégias diferentes entre chamada direta e indexação de arquivo.
- Verificação: 31 testes, evaluation `20/20` e `compileall` aprovados; hook estrutural válido.
- Pendências: avaliar remoção do chunker de domínio antigo somente após confirmar consumidores.
