## v1 — Contratos e complexidade proporcional criados

- Data/hora: 2026-10-26 -03:00.
- Status: `proposed`.
- Arquivos reais conferidos: `AGENTS.md`, `docs/instruction.md`, `.agents/skills/implementation-flow/SKILL.md`, `.agents/hooks/validate-handoffs.sh`, controles de `handoffs` e três contratos em `docs/handoff-contracts/`.
- Mudanças: contratos para sete limites, camadas estado/decisão/evidência, estado `idle`, maturidade separada, níveis `small`/`normal`/`large` e verificação de estado ativo.
- Problema resolvido: ausência de uma especificação única para limites do fluxo e risco de burocracia em tarefas pequenas.
- Verificação: hook estrutural, `bash -n`, `git diff --check` e consistência final desta rodada.

## v1 — Aplicação confirmada

- Data/hora: 2026-10-26 -03:00.
- Status: `applied`.
- Problema resolvido: contratos e complexidade proporcional passaram da análise para as regras executáveis e controles da tarefa.
- Evidência: hook retornou `handoffs válidos: 4 arquivo(s)`; `bash -n` e `git diff --check` passaram.

## v2 — Contrato 02 integrado ao fluxo

- Data/hora: 2026-10-26 -03:00.
- Status: `applied`.
- Mudanças: leitura obrigatória, aplicação no plano e validação estrutural das camadas Estado, Decisão e Evidência.
- Verificação: `bash -n`, hook com cobertura e `git diff --check` serão executados antes da finalização da tarefa.

## 022 — Finalização verificada

- Data/hora: 2026-10-26 -03:00.
- Status: `verified`.
- Arquivos reais e versões conferidos: contratos 01–03, regras oficiais, skill, hook e versões `v1`/`v2`.
- Verificação: seis arquivos de handoff válidos; `bash -n`, `git diff --check` e referências do contrato 02 aprovados.
- Resultado: fluxo proporcional e contrato estado/decisão/evidência integrados; `CURRENT.md` avançou para `idle`.

## 022 — Registro do commit

- Commit: `9a3835b` — `Integrar contratos evolutivos dos handoffs`.
- Verificação: commit criado com lista explícita de 17 arquivos da tarefa; alterações de runtime permaneceram fora do índice.
