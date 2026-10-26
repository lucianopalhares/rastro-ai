# v1 — Contratos e complexidade proporcional

- Versão-base: `021` verificada e regras reais lidas em 2026-10-26 -03:00.
- Status: `applied`; estado encontrado: contratos existiam apenas como análise; `CURRENT.md`, `handoffs/README.md` e `SEQUENCE.md` mantinham referências ativas divergentes.
- Escopo autorizado: três documentos em `docs/handoff-contracts/`, regras em `AGENTS.md`, `docs/instruction.md` e `.agents/skills/implementation-flow/SKILL.md`, além dos controles da tarefa `022`.
- Invariantes: handoffs não recebem código de aplicação; implementações anteriores permanecem preservadas; status e validação continuam explícitos.

## O que foi feito

Foram criados os contratos dos sete limites identificados, o modelo estado/decisão/evidência e as melhorias evolutivas com classificação proporcional. As regras oficiais passaram a exigir estado `idle` quando não houver tarefa aberta, separar maturidade de implementação e promover tarefas pequenas quando o risco crescer. Os controles foram ativados para a nova implementação `022` sem reabrir `021`.

## O que muda na aplicação

Não há mudança de runtime. O processo passa a ter uma referência normativa para limites, decisões e evidências, além de um fluxo enxuto para `small`, completo para `normal` e controlado por sequência para `large`. As referências ativas divergentes de `SEQUENCE.md` foram reconciliadas nesta rodada; nenhuma alteração de aplicação real foi autorizada.

## Jornada da aplicação nesta versão

Antes, o handoff organizava histórico e verificações, mas misturava regras, estado e decisão e podia exigir burocracia excessiva para mudanças pequenas. Agora, a pessoa desenvolvedora escolhe o nível proporcional, encontra os contratos em `docs/handoff-contracts/` e consegue distinguir onde a tarefa está, por que mudou e como foi demonstrada. A próxima evolução é automatizar as conferências de consistência.

## Como usar e validar a aplicação nesta versão

Para uma alteração pequena, registre objetivo, arquivos, mudança, validação e resultado. Para uma capacidade média, crie `v1` com estado, decisão e evidência. Para uma mudança grande, crie sequência e ative uma etapa por vez. Leia os três contratos e confira se a categoria escolhida é compatível com dependências, risco, número de aplicações e validação necessária.

## Cobertura por comportamento

| Comportamento | Evidência | Resultado esperado |
| --- | --- | --- |
| Os sete limites possuem contrato e limite explícitos | `docs/handoff-contracts/01-problemas-e-contratos.md` | cada problema tem garantia, limite e critério geral |
| Estado, decisão e evidência são separados | `docs/handoff-contracts/02-modelo-estado-decisao-e-evidencia.md` | cada camada tem campos, pergunta e falhas descritos |
| A complexidade do handoff é proporcional | `docs/handoff-contracts/03-melhorias-e-complexidade-proporcional.md` e regras atualizadas | `small`, `normal` e `large` possuem registros mínimos e promoção definida |
| A nova tarefa é a única ativa desta iniciativa | `CURRENT.md`, `SEQUENCE.md` e README da tarefa | todos apontam para `022` como implementação aplicada e ainda aberta |
| Runtime permanece inalterado | diff restrito a documentação e controles; integração/smoke não se aplica | nenhum arquivo de aplicação real é alterado |

## Instruções de validação

1. Execute `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/README.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/TIMELINE.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v1/README.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v1/TIMELINE.md`; resultado esperado: quatro arquivos válidos.
2. Execute `git diff --check -- AGENTS.md docs/instruction.md .agents/skills/implementation-flow/SKILL.md docs/handoff-contracts handoffs`; resultado esperado: nenhum erro de whitespace.
3. Execute `rg -n "estado|decisão|evidência|small|normal|large|idle" docs/handoff-contracts AGENTS.md docs/instruction.md .agents/skills/implementation-flow/SKILL.md`; resultado esperado: os contratos e regras proporcionais estão presentes.
4. Execute `git status --short`; resultado esperado: apenas arquivos da tarefa `022` aparecem, sem alterações de runtime incluídas por esta implementação.
5. Para finalizar, envie `skill finalizar tarefa 022`; resultado esperado: a tarefa será validada e receberá status final somente após as evidências.
