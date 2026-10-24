# v1 — Upload mínimo de arquivos

- Versão: `v1` | Versão-base: `003` (`verified`) | Status: `verified` | Data: 2026-10-23 -03:00.
- Arquivos reais conferidos: `rastro-api/src/modules/documents/domain/document.ts`, `application/create-document.use-case.ts`, `application/document.repository.ts`, `documents.module.ts`, `presentation/documents.controller.ts`, `infrastructure/in-memory-document.repository.ts`, `package.json`, `main.ts` e `.gitignore`.
- Reconciliação: itens anteriores estão aplicados na API real; upload, armazenamento e metadados de origem estavam ausentes e foram implementados diretamente.
- Alterações reais: `rastro-api/src/modules/documents/domain/document.ts`, `application/document-file.storage.ts`, `application/upload-document.use-case.ts`, `infrastructure/local-document-file.storage.ts`, `documents.module.ts`, `presentation/documents.controller.ts` e teste do caso de uso.
- Operações e âncoras: `document.ts` replace em `DocumentProperties`; `document-file.storage.ts` insert como contrato novo; `local-document-file.storage.ts` insert como adaptador novo; `upload-document.use-case.ts` insert como caso de uso novo; `documents.module.ts` replace no `DocumentsModule`; `documents.controller.ts` replace em `DocumentsController`; `upload-document.use-case.spec.ts` insert como suíte nova.
- Motivo/impacto: manter o fluxo JSON atual, criar upload multipart em `/documents/upload`, guardar bytes localmente e expor `source` no documento pendente.
- Ordem: 1) domínio e contrato; 2) armazenamento e caso de uso; 3) módulo/controller; 4) teste; 5) build, testes e smoke HTTP.
- Impacto: arquivos são gravados fora de `dist` no caminho configurável; o processamento assíncrono e a extração permanecem fora do escopo.
- Verificação: `docker compose build api`, testes do Compose com 2 suítes/7 testes e `npm run build` passaram.
- Limitações: armazenamento local em memória do documento e sem job de indexação; produção deverá substituir o adaptador por object storage.

## Instruções de validação

1. Execute `docker compose build api`; o build da API deve concluir sem erro.
2. Execute `docker compose run --rm --no-deps api npm test -- --runInBand`; as 2 suítes e os 7 testes devem passar.
3. Execute `docker compose run --rm --no-deps api npm run build`; a compilação NestJS deve concluir sem erro.
4. Crie um arquivo de teste: `printf '%s\n' '# Decision' 'Use PostgreSQL.' > /tmp/meeting.md`.
5. Execute `curl -i -X POST http://localhost:3039/api/v1/documents/upload -F 'projectId=project-1' -F 'file=@/tmp/meeting.md;type=text/markdown'`; a resposta deve ser `HTTP/1.1 201` com `status: "pending"` e `source.storageKey` terminado em `.md`.
6. Execute `curl -i -X POST http://localhost:3039/api/v1/documents/upload -F 'projectId=project-1' -F 'file=@/tmp/meeting.md;filename=meeting.pdf;type=application/pdf'`; a resposta deve ser `HTTP/1.1 400`.
