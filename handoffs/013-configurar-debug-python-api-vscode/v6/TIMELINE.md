# Timeline — 013/v6

## v6 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: controller de upload, manifest, README da API e logs do container.
- Mudança aplicada: fallback `request.file` adicionado ao handler, mantendo `@UploadedFile()`.
- Problema resolvido: `@UploadedFile()` chegava `undefined` e retornava `A file is required`.
- Pendências: rebuild da API e novo smoke HTTP do upload.
