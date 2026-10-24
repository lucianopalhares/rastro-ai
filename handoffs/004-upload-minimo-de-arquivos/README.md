# 004 — Upload mínimo de arquivos

- Data/hora: 2026-10-23 -03:00 | Status: `verified`
- Aplicação afetada: `api` (`rastro-api`)
- Dependência/ordem: `003` verificada; próxima etapa `005-extracao-e-chunking`.
- Objetivo: receber arquivos `.md` e `.txt`, armazená-los localmente e associá-los ao documento criado.
- Evolução: `v1` aplicou diretamente o contrato multipart, armazenamento local configurável, caso de uso, endpoint e testes.
- Impactos: cria arquivos em `DOCUMENT_STORAGE_PATH` ou `storage/documents`; não inicia indexação nem altera o endpoint JSON existente.
- Critério: atendido; upload válido, extensão inválida e conteúdo vazio estão cobertos, com testes e build aprovados.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/` | Próxima ação: iniciar a etapa `005-extracao-e-chunking`.
