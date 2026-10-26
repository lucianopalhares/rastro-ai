## v2 — Contrato 02 integrado ao fluxo

- Data/hora: 2026-10-26 -03:00.
- Status: `applied`.
- Arquivos reais: `AGENTS.md`, `docs/instruction.md`, `.agents/skills/implementation-flow/SKILL.md`, `.agents/hooks/validate-handoffs.sh` e o contrato 02.
- Mudanças: leitura obrigatória antes do planejamento/verificação, aplicação explícita no fluxo e proteção estrutural das três camadas.
- Problema resolvido: o contrato existia, mas podia ser ignorado pelo fluxo operacional.
- Verificação: `bash -n`, hook com cobertura e `git diff --check` pendentes nesta rodada.
