# 004 — Upload mínimo de arquivos

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: `api` (`rastro-api`)
- Dependência/ordem: `003` verificada; próxima etapa `005-extracao-e-chunking`.
- Objetivo: receber arquivos `.md` e `.txt`, armazená-los localmente e associá-los ao documento criado.
- Evolução: `v1` aplicou diretamente o contrato multipart, armazenamento local configurável, caso de uso, endpoint e testes; `v2` adicionou fixture versionado; `v3` converteu o fixture em transcrição natural; `v4` confirmou o smoke HTTP com resposta `201`.
- Impactos: cria arquivos em `DOCUMENT_STORAGE_PATH` ou `storage/documents`; não inicia indexação nem altera o endpoint JSON existente.
- Critério: implementação original e fixture de transcrição verificados; smoke HTTP retornou `201` e documento `pending`.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/` | Próxima ação: usar o fixture em simulações ou iniciar a etapa `005-extracao-e-chunking`.
