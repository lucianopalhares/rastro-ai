# 002 — Adicionar controller de documentos

Versão: `v4` | Versão-base: `v3` | Data/hora: 2026-10-23 -03:00 | Status: `proposed`
Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/modules/documents/documents.module.ts` e o diretório `presentation/`.
Reconciliação: o módulo já importa/registra `DocumentsController`, mas o arquivo real está ausente; existe apenas um artefato `.handoff.md` dentro da aplicação.
Pendência: criar `src/modules/documents/presentation/documents.controller.ts`; não remover o artefato existente nesta rodada.
Ordem: aplicar o arquivo e executar build, boot e chamadas HTTP; critério: compilação sem `TS2307` e endpoints de documentos funcionais.
