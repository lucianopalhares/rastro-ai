# Linha do tempo — 004 Upload mínimo de arquivos

## v1 — 2026-10-23 -03:00

- Status: `proposed` | Versão-base: implementação `003` em status `verified`.
- Arquivos conferidos: `document.ts`, `documents.controller.ts`, `documents.module.ts`, `create-document.use-case.ts`, `document.repository.ts`, `package.json`, `main.ts`, `.gitignore` e Compose reais.
- Reconciliação: o fluxo JSON existente foi considerado preservado; não havia endpoint de upload, abstração de armazenamento ou associação de arquivo.
- Mudança proposta: adicionar contrato de armazenamento, adaptador local, caso de uso multipart, metadados opcionais no documento e testes unitários.
- Problema resolvido: ausência de recebimento e persistência mínima de arquivos `.md` e `.txt` vinculados a um projeto/documento.
- Pendências: aplicação manual, teste HTTP multipart e confirmação dos limites de armazenamento local.
- Verificação prevista: `npm test`, `npm run build` e chamada multipart com arquivo válido e inválido.

## v1 — 2026-10-23 -03:00 — Verificação

- Status: `verified` | A implementação foi aplicada diretamente na API real; o registro permanece sem código copiável.
- Arquivos alterados: domínio, contrato de armazenamento, adaptador local, caso de uso, módulo, controller e teste unitário.
- Comentários: classes, interfaces, construtores, métodos e cenários alterados receberam JSDoc com descrição e histórico `v1`.
- Verificação: `docker compose build api` passou; `docker compose run --rm --no-deps api npm test -- --runInBand` passou com 2 suítes e 7 testes; build passou.
- Impacto: upload multipart limitado a 5 MiB, extensões `.md`/`.txt`, conteúdo não vazio e associação por `source.storageKey`.
- Pendências: smoke HTTP multipart e substituição futura do armazenamento local por object storage permanecem fora desta rodada.

## Finalização — 2026-10-23 -03:00

- Status: `verified` | Todas as versões existentes foram conferidas; a `v1` está aplicada diretamente e verificada.
- Verificação adicional: smoke HTTP válido retornou `201` com `pending` e `source.storageKey`; extensão `.pdf` retornou `400`.
- Limitações: armazenamento local e indexação assíncrona continuam como responsabilidades das próximas etapas.
- Avanço: `CURRENT.md` será atualizado para `005`, conforme a sequência registrada.
