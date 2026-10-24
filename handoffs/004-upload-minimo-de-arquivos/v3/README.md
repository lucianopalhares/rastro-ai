# v3 — Transcrição natural para simulação de upload

- Versão: `v3` | Versão-base: `v2` (`applied`) | Status: `applied` | Data: 2026-10-24 -03:00.
- Arquivo real conferido: `rastro-api/test/fixtures/upload/meeting.md`; o fixture anterior continha tópicos estruturados, mas a simulação desejada exige fala contínua.
- Contexto encontrado: `v2` criou o arquivo reutilizável e o endpoint permanece inalterado, aceitando `.md` não vazio.
- Alteração real: substituído o conteúdo por uma transcrição curta, sem estrutura de tópicos, com três participantes e decisão ao final.
- Operação/âncora: replace no conteúdo de `rastro-api/test/fixtures/upload/meeting.md`; nenhuma alteração no código da API.
- Motivo/impacto: aproximar o fixture do formato esperado de uma reunião real e permitir testes futuros de extração de conversa.
- Dependências/pendências: smoke HTTP e futura extração continuam dependendo das etapas ou serviços correspondentes.

## Instruções de validação

1. Execute `test -s rastro-api/test/fixtures/upload/meeting.md`; resultado esperado: código `0`.
2. Execute `rg -n 'Marina:|Rafael:|João:' rastro-api/test/fixtures/upload/meeting.md`; resultado esperado: encontrar falas dos três participantes.
3. Com a API em execução, execute `curl -i -X POST http://localhost:3039/api/v1/documents/upload -F 'projectId=project-1' -F 'file=@rastro-api/test/fixtures/upload/meeting.md;type=text/markdown'`; resultado esperado: `HTTP/1.1 201` com `status: "pending"`.
