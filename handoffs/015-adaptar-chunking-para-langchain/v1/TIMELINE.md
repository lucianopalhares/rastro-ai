## v1 — Tarefa proposta

- Data/hora: 2026-10-25 -03:00.
- Status: `proposed`.
- Aplicação: serviço Python `rastro-ai`.
- Plano: usar `TextChunker` no caso de uso e encapsular `langchain-text-splitters` em adaptador de infraestrutura.
- Invariantes: preservar chunks, offsets, projeto, índice, sobreposição, tokens e baseline.
- Pendências: validar versão da biblioteca, offsets e diferenças de avaliação antes de alterar o runtime.
- Verificação prevista: testes, evaluation, compilação, smoke e hook estrutural.
