# v2 — Fixture versionado para simulação de upload

- Versão: `v2` | Versão-base: `v1` (`verified`) | Status: `applied` | Data: 2026-10-24 -03:00.
- Arquivo real conferido: `rastro-api/src/modules/documents/presentation/documents.controller.ts`; o contrato aceita campo `file`, `projectId` e arquivos `.md`/`.txt` não vazios.
- Contexto encontrado: a implementação `004` já estava verificada; faltava um conteúdo reutilizável versionado para smoke tests manuais.
- Alteração real: criado `rastro-api/test/fixtures/upload/meeting.md` com conteúdo textual estável para upload.
- Operação/âncora: novo fixture em `rastro-api/test/fixtures/upload/`, separado do armazenamento gerado em `rastro-api/storage/documents`.
- Motivo/impacto: permitir simulações futuras sem criar conteúdo temporário; não altera API, domínio, armazenamento ou testes automatizados.
- Dependências/pendências: API em execução em `http://localhost:3039`; nenhuma pendência funcional conhecida.

## Instruções de validação

1. Confirme que o arquivo existe e é não vazio: `test -s rastro-api/test/fixtures/upload/meeting.md`; resultado esperado: código `0`.
2. Com a API em execução, execute `curl -i -X POST http://localhost:3039/api/v1/documents/upload -F 'projectId=project-1' -F 'file=@rastro-api/test/fixtures/upload/meeting.md;type=text/markdown'`; resultado esperado: `HTTP/1.1 201`, `status: "pending"` e `source.storageKey` terminado em `.md`.
