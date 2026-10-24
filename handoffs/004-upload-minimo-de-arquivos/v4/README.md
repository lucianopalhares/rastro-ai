# v4 — Verificação do upload da transcrição

- Versão: `v4` | Versão-base: `v3` (`applied`) | Status: `verified` | Data: 2026-10-24 -03:00.
- Evidência recebida: `curl` executado contra `http://localhost:3039/api/v1/documents/upload` usando `rastro-api/test/fixtures/upload/meeting.md`.
- Resultado: `HTTP/1.1 201 Created`, documento criado para `project-1`, conteúdo da transcrição preservado e `status: "pending"`.
- Arquivo conferido: `rastro-api/test/fixtures/upload/meeting.md`; o `source.storageKey` retornou identificador terminado em `.md`.
- Alteração de código: nenhuma; esta rodada apenas registra a verificação manual bem-sucedida do fixture e do endpoint já implementado.
- Pendências: processamento assíncrono/indexação continuam fora do escopo do upload mínimo.

## Instruções de validação

1. Execute `curl -i -X POST http://localhost:3039/api/v1/documents/upload -F 'projectId=project-1' -F 'file=@rastro-api/test/fixtures/upload/meeting.md;type=text/markdown'`; resultado esperado: `HTTP/1.1 201 Created`, `status: "pending"`, `name: "meeting.md"` e `source.storageKey` terminado em `.md`.
