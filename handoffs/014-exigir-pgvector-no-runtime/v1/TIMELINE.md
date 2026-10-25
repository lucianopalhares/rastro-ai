## v1 — Tarefa proposta

- Data/hora: 2026-10-25 -03:00.
- Status: `proposed`.
- Arquivos reais previstos para reconciliação: serviço de seleção do backend, adaptadores de retrieval, testes, Compose, schema e documentação da IA.
- Mudança planejada: exigir `PostgresVectorStore` com embeddings no runtime e retirar a seleção lexical implícita.
- Problema: `InMemoryVectorStore` pode ser escolhido sem configuração e não representa busca semântica.
- Pendências: comparar as âncoras com o estado real e implementar somente na próxima rodada autorizada.
- Verificação prevista: testes unitários, compilação Python, configuração Compose, smoke com pgvector e validação estrutural.
