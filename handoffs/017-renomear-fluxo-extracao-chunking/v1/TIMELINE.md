## v1 — Renomeação aplicada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: caso de uso, container, fachadas, serviço HTTP, exports, testes, README e documentação arquitetural conferidos.
- Mudanças: nomes antigos substituídos por `extract_and_chunk_document`, `index_document_chunks` e `ExtractAndChunkDocumentUseCase`.
- Problema resolvido: separação semântica entre gerar chunks e persistir chunks vetorizados.
- Verificação prevista: 36 testes, evaluation `20/20`, compilação, busca de referências e hook estrutural.
- Pendências: confirmar consumidores externos dos nomes antigos antes da finalização.
