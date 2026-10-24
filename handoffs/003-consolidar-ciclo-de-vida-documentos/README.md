# 003 — Consolidar ciclo de vida dos documentos

- Data/hora: 2026-10-23 -03:00 | Status: `verified`
- Aplicação afetada: `api` (`rastro-api`)
- Dependência/ordem: `002` considerada concluída | primeira tarefa da continuação da Fase 1
- Objetivo: formalizar projeto, estados de indexação e transições do agregado `Document`.
- Evolução: `v1` propôs o contrato; `v2` corrigiu os caminhos; `v3` reconcilia a aplicação parcial; `v4` corrige o Compose; `v5` foi descartada; `v6` configura Jest; `v7` explicita os tipos globais do Jest no TypeScript.
- Impactos: prepara o contrato para upload e indexação, mantém a execução local em `rastro-api` e registra a verificação reproduzível.
- Critério: build, testes do domínio e validação HTTP de `projectId`, `name` e `content` passarem.
- Pendências: nenhuma pendência técnica desta implementação; próxima etapa ativada: `004-upload-minimo-de-arquivos`.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/`
