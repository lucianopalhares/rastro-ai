# Timeline — 013/v5

## v5 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: controller de upload, manifest da API, README e container Docker.
- Mudança aplicada: `projectId` passou a ser validado isoladamente no body; `file` permanece em `@UploadedFile()`.
- Problema resolvido: HTTP `400` `property file should not exist` mesmo com Multer instalado.
- Pendências: reconstruir a API e repetir o `curl`; confirmar o status final conforme embeddings disponíveis.
