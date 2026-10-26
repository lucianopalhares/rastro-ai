# v1 — Regras de comentários e contrato mínimo

- Versão-base: regras existentes em `AGENTS.md`, `docs/instruction.md` e `.agents/skills/implementation-flow/SKILL.md`; leitura real em 2026-10-26 -03:00.
- Status: `applied`; estado encontrado: fluxo de início, finalização e versões preservado, com duplicação de regras e histórico de comentários sem o número da tarefa.
- Escopo autorizado: regras de handoff, skill operacional e controles da implementação `021`; fora do escopo estão aplicações e alterações locais de código não relacionadas.
- Invariantes: comandos explícitos, `CURRENT.md`, versões `vN`, status existentes, reconciliação e aplicação direta nos arquivos reais permanecem.

## O que foi feito

Foi atualizada a política em `/home/dev/dev/ia/rastro-ai/docs/instruction.md`, as orientações gerais em `/home/dev/dev/ia/rastro-ai/AGENTS.md` e o procedimento em `/home/dev/dev/ia/rastro-ai/.agents/skills/implementation-flow/SKILL.md`. Os comentários agora priorizam comportamento e motivo em linguagem simples, usam histórico `NNN-vN` e não são exigidos para alterações puramente mecânicas. O contrato mínimo da versão passou a registrar estado-base, escopo autorizado, invariantes, mudança aplicada e evidência.

## O que muda na aplicação

Não há mudança de runtime ou comportamento das aplicações. O fluxo de iniciar, continuar, versionar e finalizar tarefas permanece o mesmo; a documentação fica mais enxuta e explícita, e a consistência entre `CURRENT.md`, `SEQUENCE.md`, README e timelines passa a ser conferida antes da entrega. As alterações locais em `rastro-ai` foram preservadas fora do escopo.

## Jornada da aplicação nesta versão

Antes, o agente já controlava tarefas por handoffs, versões e status, mas os comentários podiam repetir detalhes técnicos e o histórico `v1` não identificava a tarefa. Agora, uma pessoa consegue entender o motivo e o efeito das partes importantes do código e localizar a origem de uma mudança por `NNN-vN`. A evolução é documental e não altera a capacidade funcional da aplicação.

## Como usar e validar a aplicação nesta versão

Não há endpoint, tela ou fluxo de runtime novo para usar. Para validar a capacidade, leia as três regras atualizadas e confira um comentário alterado ou criado: ele deve explicar o que faz, por que existe e usar o identificador da tarefa, como `021-v1`. A validação executável está na seção seguinte.

## Cobertura por comportamento

| Comportamento | Evidência | Resultado esperado |
| --- | --- | --- |
| Comentário semântico usa linguagem simples e `NNN-vN` | inspeção textual das três regras | regra presente e sem exigência para ajustes mecânicos |
| Fluxo de início, versões e finalização permanece preservado | comparação textual com as regras anteriores | comandos, status e avanço não são substituídos |
| Estado ativo aponta para a nova tarefa | `CURRENT.md`, `SEQUENCE.md` e README | todos indicam `021` como ativo |
| Runtime das aplicações permanece inalterado | `git diff` restrito aos arquivos da tarefa | nenhum arquivo de aplicação entra na mudança |

## Instruções de validação

1. Execute `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/021-revisar-fluxo-e-comentarios-handoffs/README.md handoffs/021-revisar-fluxo-e-comentarios-handoffs/TIMELINE.md handoffs/021-revisar-fluxo-e-comentarios-handoffs/v1/README.md handoffs/021-revisar-fluxo-e-comentarios-handoffs/v1/TIMELINE.md`; resultado esperado: `handoffs válidos: 4 arquivo(s)`.
2. Execute `git diff --check -- AGENTS.md docs/instruction.md .agents/skills/implementation-flow/SKILL.md handoffs/README.md handoffs/CURRENT.md handoffs/SEQUENCE.md handoffs/TIMELINE.md handoffs/021-revisar-fluxo-e-comentarios-handoffs`; resultado esperado: nenhum erro de whitespace.
3. Execute `git status --short`; resultado esperado: somente os arquivos desta tarefa e as duas alterações locais de código já existentes aparecem, sem arquivos de aplicação adicionados por esta implementação.
4. Confira a ordem das seções deste README: `O que foi feito`, `O que muda na aplicação`, `Jornada`, `Como usar`, `Cobertura` e `Instruções de validação`; resultado esperado: ordem preservada.
5. Envie `skill finalizar tarefa 021`; resultado esperado: a implementação ativa é conferida, recebe status final conforme as evidências e só então `CURRENT.md` pode avançar.
