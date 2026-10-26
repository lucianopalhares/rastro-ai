# v2 — Integração operacional do contrato de estado, decisão e evidência

- Versão-base: `v1` aplicada; arquivos reais relidos em 2026-10-26 -03:00.
- Estado encontrado: o contrato `02-modelo-estado-decisao-e-evidencia.md` já existia e era referenciado, mas não era leitura obrigatória nem requisito do hook.
- Escopo autorizado: integrar o contrato 02 em `AGENTS.md`, `docs/instruction.md`, `.agents/skills/implementation-flow/SKILL.md` e `.agents/hooks/validate-handoffs.sh`; preservar v1 e os demais contratos.
- Invariantes: não copiar código para handoffs, não alterar runtime e manter estado/decisão/evidência como camadas distintas.

## O que foi feito

Foi adicionada a leitura obrigatória do contrato 02 ao início do fluxo, sua aplicação explícita ao plano e à validação, e uma checagem estrutural que exige o arquivo e as três seções de camada. A documentação consolidada da tarefa passou a registrar a evolução `v1` → `v2`.

## O que muda na aplicação

Não há mudança de runtime. Antes de planejar ou verificar uma tarefa, o agente deve ler e aplicar o contrato de estado, decisão e evidência; o hook falha se o contrato desaparecer ou perder uma das três camadas. Os contratos 01 e 03 continuam preservados e consultivos conforme o escopo.

## Jornada da aplicação nesta versão

Antes, o contrato 02 era uma referência documental disponível, mas sua leitura dependia da disciplina do agente. Agora, ele participa do fluxo obrigatório e possui uma proteção estrutural mínima, reduzindo o risco de uma rodada registrar apenas operações sem contexto ou evidência. A próxima evolução continua sendo automatizar a coerência entre os campos e os resultados reais.

## Como usar e validar a aplicação nesta versão

Ao iniciar ou continuar uma tarefa, leia `docs/handoff-contracts/02-modelo-estado-decisao-e-evidencia.md` antes de planejar. Preencha estado, decisão e evidência no handoff aplicável. Execute o hook com os quatro arquivos da tarefa; ele deve confirmar a existência do contrato e das seções `Camada 1 — Estado`, `Camada 2 — Decisão` e `Camada 3 — Evidência`.

## Cobertura por comportamento

| Comportamento | Evidência | Resultado esperado |
| --- | --- | --- |
| O contrato 02 é leitura obrigatória no fluxo | `AGENTS.md`, `docs/instruction.md` e `.agents/skills/implementation-flow/SKILL.md` | os três pontos instruem a leitura ou aplicação do documento |
| O contrato 02 é protegido estruturalmente | `.agents/hooks/validate-handoffs.sh` | hook exige arquivo e três camadas |
| A rodada mantém o estado/decisão/evidência separados | contrato 02 e README desta versão | plano e validação usam as três camadas sem alterar o runtime |
| Implementações anteriores permanecem intactas | `v1` e diff restrito ao fluxo | v1 não é sobrescrita e os contratos 01 e 03 permanecem |

## Instruções de validação

1. Execute `bash -n .agents/hooks/validate-handoffs.sh`; resultado esperado: sucesso sem saída.
2. Execute `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/README.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/TIMELINE.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v1/README.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v1/TIMELINE.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v2/README.md handoffs/022-contrato-evolutivo-do-fluxo-de-handoffs/v2/TIMELINE.md`; resultado esperado: oito arquivos válidos.
3. Execute `git diff --check -- AGENTS.md docs/instruction.md .agents/skills/implementation-flow/SKILL.md .agents/hooks/validate-handoffs.sh docs/handoff-contracts handoffs`; resultado esperado: nenhum erro de whitespace.
4. Execute `rg -n "02-modelo-estado-decisao-e-evidencia|Camada 1|Camada 2|Camada 3" AGENTS.md docs/instruction.md .agents/skills/implementation-flow/SKILL.md .agents/hooks/validate-handoffs.sh`; resultado esperado: contrato e três camadas aparecem no fluxo e no hook.
5. Para finalizar a implementação inteira, envie `skill finalizar tarefa 022`; resultado esperado: v1 e v2 serão conferidas antes do status final e do commit.
