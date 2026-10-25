## v2 — Adaptador aplicado

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai`.
- Mudanças: contrato `TextChunker` formalizado, caso de uso desacoplado e adaptador `RecursiveCharacterTextSplitter` criado na infraestrutura.
- Compatibilidade: `DocumentChunk`, offsets, índice, projeto, sobreposição e fachada legada preservados nos testes; baseline `20/20`.
- Verificação: 30 testes, evaluation e `compileall` aprovados; hook final executado após a criação deste registro.
- Pendências: smoke API → Python → pgvector e medição de custo/latência ficam para a finalização da tarefa.
