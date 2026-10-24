---
name: implementation-flow
description: "Administra implementações isoladas do Rastro AI, aplicando mudanças diretamente nas aplicações e registrando o ciclo em handoffs numerados."
---

# Implementation Flow

Esta skill só pode ser usada quando a mensagem do usuário contiver explicitamente uma destas formas:

- `skill iniciar tarefa ...`;
- `skill finalizar tarefa <numero>`.

Não invoque esta skill para pedidos sem o prefixo `skill`, mesmo que o pedido pareça relacionado a uma implementação. Nesses casos, siga somente `AGENTS.md`, `docs/instruction.md` e a implementação indicada por `CURRENT.md`.

Discussões não geram handoffs. Antes de criar ou atualizar arquivos, resuma o plano e aguarde autorização explícita; se houver ambiguidade, permaneça em discussão.

## Objetivo

Controlar o ciclo de vida de implementações do projeto aplicando as mudanças diretamente nos arquivos reais. A saída em `handoffs/` contém somente contexto, status e histórico em `README.md` e `TIMELINE.md`; não contém cópias de código. Alterações solicitadas em `.agents/`, `docs/` ou `AGENTS.md` também podem ser feitas diretamente.

Todo código criado ou alterado pela skill deve usar inglês nos nomes de classes, métodos, funções, variáveis, propriedades, interfaces, tipos, enums, módulos e arquivos de código. Os comentários de versionamento no código e o texto instrucional dos registros — localização, motivo, impacto, dependências e verificações — devem ser escritos em pt-BR.

## Arquivos de controle

Antes de agir, leia:

1. `/home/dev/dev/ia/rastro-ai/AGENTS.md`;
2. `/home/dev/dev/ia/rastro-ai/docs/instruction.md`;
3. `/home/dev/dev/ia/rastro-ai/handoffs/CURRENT.md`;
4. o `README.md` da implementação apontada por `CURRENT.md`, quando existir.

Também leia `handoffs/SEQUENCE.md` quando existir. Ele é a fonte da ordem entre tarefas, mas não é fonte do código.

Não use os registros de versões anteriores como fonte do código atual. Leia e altere o código somente nas aplicações reais do projeto; use os README e timelines apenas para identificar o histórico e o estado da tarefa.

Consulte documentos em `docs/fases/` somente quando forem relevantes para entender o escopo. Eles são referência, não destino de alterações.

## Estrutura obrigatória

Cada implementação deve ser uma unidade isolada:

```text
handoffs/
├── CURRENT.md
├── TIMELINE.md
├── README.md
└── 001-titulo-da-implementacao/
    ├── README.md
    └── v1/
        ├── README.md
        └── TIMELINE.md
```

Use o próximo número disponível, com três dígitos, e um título em `kebab-case`.

Os handoffs desta skill são registros compactos. O código, configuração, testes e documentação permanecem e são alterados diretamente nas aplicações reais. O README da implementação, `CURRENT.md` e os timelines são arquivos de controle.

- `vN/README.md`: resumo, arquivos reais alterados, operações, comentários de versão, verificações e a seção obrigatória `## Instruções de validação`;
- `vN/TIMELINE.md`: histórico append-only da rodada; antes da entrega, as entradas inteiras devem estar em ordem cronológica sem alteração de conteúdo.

## Decidir entre continuar e iniciar

Leia o número em `CURRENT.md` e o status no README da implementação.

As duas formas válidas para esta skill são:

- `skill iniciar tarefa sobre X`: criar uma nova implementação para X;
- `skill finalizar tarefa 001`: finalizar a implementação indicada.

O número informado pelo usuário tem prioridade para localizar uma implementação específica. A continuidade de uma implementação sem essas frases não ativa esta skill; nesse caso, o fluxo normal usa `CURRENT.md`.

Continue na implementação atual quando:

- o usuário indicar explicitamente que deseja continuar;
- o novo pedido for parte do mesmo objetivo;
- os arquivos ainda estiverem em `proposed` ou `approved`.

Crie uma nova implementação quando:

- o usuário disser “iniciar nova implementação”;
- o usuário disser “iniciar tarefa”;
- o usuário fornecer um novo título;
- o objetivo for diferente;
- a implementação anterior estiver `verified`, `rolled-back` ou encerrada;
- o usuário pedir uma correção de uma implementação anterior.

Uma correção histórica cria uma nova implementação que referencia a anterior. Nunca altere a pasta antiga.

## Dividir solicitações grandes

Antes de criar handoffs, avalie se a solicitação deve virar uma sequência de tarefas. Divida quando houver muitos arquivos, mais de uma aplicação, etapas dependentes, contratos diferentes, validações independentes ou um handoff difícil de revisar.

Cada implementação deve conter uma única capacidade ou etapa aplicável, poucos arquivos relacionados, critério de conclusão próprio e ordem explícita. Divida por resultado verificável, não apenas por arquivo. Uma implementação posterior pode declarar dependência de outra pelo número, mas não pode copiar seus handoffs nem alterar sua pasta.

No README de cada etapa, registre, quando aplicável, a iniciativa relacionada, dependências, posição na ordem, próxima etapa e critério de conclusão. `CURRENT.md` aponta somente para a etapa ativa; ao terminar uma etapa, a próxima pode ser ativada preservando o histórico anterior.

Quando a solicitação gerar várias etapas, primeiro defina a sequência completa, as dependências, os pré-requisitos e os critérios de conclusão. Ative somente a primeira etapa e aplique apenas essa etapa na aplicação real. As demais podem ser registradas como planejadas, mas não devem ser aplicadas ou ativadas antecipadamente.

Não pule etapas. Só avance depois de receber `skill finalizar tarefa <numero>` para a etapa atual e confirmar status `applied` ou `verified`. Nesse momento, atualize `CURRENT.md` para a próxima etapa da sequência. Se o usuário pedir uma etapa posterior antes da conclusão da atual, recuse o salto, explique a dependência e mantenha a etapa atual ativa.

Pedidos diretos para iniciar ou continuar uma etapa posterior não autorizam um salto. Mantenha `CURRENT.md` e `SEQUENCE.md` inalterados e indique a tarefa bloqueadora.

Se nenhuma palavra de comando for usada, não crie uma implementação nova por inferência: use `CURRENT.md`. Pergunte somente quando `CURRENT.md` estiver inválido, ausente ou quando o número solicitado não existir.

O usuário não precisa criar pastas manualmente. Ao iniciar uma implementação, crie a nova pasta, `v1/README.md` e `v1/TIMELINE.md`, atualize `CURRENT.md` somente com o novo número e crie o README da implementação.

## Criar uma implementação

Ao iniciar uma nova implementação:

1. encontre o maior número já usado;
2. escolha o próximo número disponível;
3. crie `handoffs/<numero-titulo>/v1/`;
4. crie o README compacto da implementação, com no máximo 8 linhas;
5. registre o título e, nas linhas seguintes, cada campo como item de lista Markdown iniciado por `- `: data/hora, status, aplicação afetada, dependência/ordem, motivo, impactos, resolução/critério e pasta relacionada, combinando campos para manter no máximo 8 linhas;
6. defina o status inicial como `proposed`;
7. atualize `CURRENT.md` somente com o número;
8. acrescente uma entrada compacta de no máximo 8 linhas ao final de `TIMELINE.md`;
9. aplique diretamente as alterações nos arquivos reais e registre os caminhos no README da versão.

Se a solicitação tiver várias etapas, registre primeiro todas elas em `handoffs/SEQUENCE.md`, mas detalhe e ative somente a primeira. Ao finalizar uma etapa válida, atualize `CURRENT.md` para a próxima etapa registrada, sem permitir saltos.

Não copie arquivos, handoffs ou README de implementações anteriores. Uma nova implementação começa somente com o contexto necessário para o novo objetivo.

## Criar um handoff

Para cada arquivo que precisar ser alterado, edite diretamente o arquivo real. No README da versão, registre o caminho, a operação, a âncora, o impacto e a verificação. Não copie o arquivo para `handoffs/`.

### Rodada de continuação

Ao continuar uma implementação, determine a maior versão existente e crie uma nova versão, nunca reutilizando a pasta anterior. Leia o README da tarefa, o README da versão-base e os arquivos reais das aplicações. Compare cada handoff anterior com o arquivo real e registre o resultado como `aplicado`, `parcial`, `divergente` ou `ausente`. A versão anterior não é fonte de código nem evidência de aplicação.

Só altere arquivos que ainda sejam necessários no estado real. Preserve trechos já aplicados e reavalie a operação com base no código atual. O README da nova versão deve registrar a versão-base, a data da leitura dos arquivos reais, o inventário de reconciliação, as mudanças feitas, as pendências e a verificação esperada.

O README de cada versão deve registrar:

- caminho absoluto do arquivo original;
- número de linha como referência auxiliar;
- função, classe, método, import, chave ou seção;
- operação: `insert`, `replace` ou `remove`;
- comentário JSDoc em pt-BR, no formato `/** ... */`, acima de toda classe, interface, método, função, contrato ou bloco alterado; o comentário deve explicar o que o elemento faz, por que existe e manter histórico acumulado com `v1`, `v2` etc. para cada mudança;
- o que o trecho faz;
- por que deve ser inserido, substituído ou removido;
- comportamento alterado;
- o que permanece inalterado;
- testes, evaluation e verificações.

O README de cada versão deve conter obrigatoriamente a seção `## Instruções de validação`, com cada comando, URL, ação manual ou teste necessário, além do resultado esperado para confirmar o comportamento alterado. Para toda requisição HTTP, o registro deve incluir um comando completo copiável, como `curl`, com método, URL, headers, payload ou campos multipart, arquivo de entrada e resposta esperada.

Antes de entregar, confira os dois timelines e realinhe apenas a posição das entradas inteiras para a ordem cronológica correta. Não edite o texto, status, data ou conteúdo das entradas históricas durante esse realinhamento.

Os arquivos de saída do handoff são somente `README.md` e `TIMELINE.md`; o caminho real do arquivo alterado deve aparecer no README.

O número de linha nunca é suficiente sozinho. Use o ponto estrutural e o comentário versionado no arquivo real para que a mudança permaneça identificável.

## Ordem entre aplicações

Quando houver mais de uma aplicação, documente a ordem no README e nos handoffs:

1. API, banco ou contratos;
2. serviço Python de IA;
3. worker ou MCP;
4. frontend;
5. evaluation e observabilidade.

Explique dependências como “a API precisa ser aplicada antes da tool Python” ou “o backend precisa publicar o contrato antes do frontend consumi-lo”.

## Status

Use somente:

- `proposed`: handoff criado, ainda não aprovado;
- `approved`: responsável aprovou a aplicação;
- `applied`: alterações foram aplicadas aos arquivos originais;
- `verified`: testes e verificações passaram;
- `rolled-back`: aplicação foi revertida.

`approved`, `applied` e `verified` exigem confirmação ou evidência. `applied` exige confirmação explícita da aplicação. `verified` exige comandos e resultados registrados. Aplicação parcial mantém a tarefa ativa e impede o avanço.

Atualize o status no README da implementação. Para cada mudança de status, acrescente uma nova entrada compacta, de no máximo 8 linhas, ao final de `TIMELINE.md`; não reescreva entradas antigas.

## Continuar uma implementação

Ao continuar a implementação apontada por `CURRENT.md`:

1. leia o README e os arquivos atuais das aplicações reais;
2. preserve os handoffs já criados sem lê-los como fonte do código atual;
3. adicione somente novos trechos necessários com base no código real;
4. não reescreva o histórico;
5. atualize somente os campos compactos permitidos no README, mantendo-o com no máximo 8 linhas;
6. acrescente observações à timeline apenas no final.

Antes de adicionar novos handoffs, compare as âncoras com os arquivos reais. Se houver divergência, aplicação parcial ou alterações locais não relacionadas, pare e registre a pendência para decisão do responsável. Não use handoffs anteriores como evidência do estado atual.

Uma implementação pode ter sido aplicada parcialmente antes de ser retomada. Por isso, a skill deve reler a pasta real da aplicação e o arquivo original afetado antes de criar, recriar ou ajustar um handoff, mesmo que já exista uma proposta anterior para o mesmo arquivo. O agente deve comparar o estado encontrado, preservar trechos já aplicados e gerar somente a diferença necessária; se o arquivo já existir, deve reavaliar a operação e as âncoras, convertendo `insert` em `replace` quando necessário. Snippets e handoffs antigos servem apenas como histórico e não podem ser usados para reconstruir o código atual.

Se o pedido mudar o objetivo, pare e crie uma nova implementação.

## Finalizar uma implementação

Quando o usuário disser para finalizar, concluir ou encerrar:

1. confirme os registros e a ordem de execução;
2. registre testes e evaluation executados, se houver;
3. registre limitações e próximos passos nos registros, quando necessários;
4. atualize o README para `verified`, `applied` ou `rolled-back`, conforme evidência;
5. acrescente uma entrada compacta de conclusão, com no máximo 8 linhas, ao final da timeline;
6. não altere a pasta finalizada depois disso;
7. se existir uma próxima etapa em `SEQUENCE.md`, atualize `CURRENT.md` para ela somente após a etapa estar `applied` ou `verified`;
8. confirme que todas as versões existentes da implementação foram conferidas e estão com status final (`applied` ou `verified`);
9. monte uma lista explícita dos arquivos da tarefa a partir dos handoffs, da aplicação real e dos controles da implementação; alterações não relacionadas devem ficar fora da lista e não impedem o commit;
10. adicione somente a lista explícita, usando `git add -f` apenas quando um handoff da própria tarefa estiver ignorado, e gere o commit automático se todas as condições da tarefa forem atendidas, usando mensagem e corpo em pt-BR;
11. monte o resumo do commit a partir do `TIMELINE.md` da implementação e do `README.md` consolidado, cobrindo todas as versões;
12. registre na timeline da implementação o identificador do commit, a mensagem e a verificação executada;
13. a próxima mudança deve respeitar a etapa apontada por `CURRENT.md`.

Se houver versão sem status final, pendência de aplicação, divergência não resolvida ou arquivo da própria tarefa que não possa ser identificado com segurança, não gere o commit automático. Alterações não relacionadas devem apenas ser deixadas fora do índice. Registre o bloqueio e mantenha a implementação ativa até que o responsável resolva a pendência.

## Restrições

- nunca copiar código de aplicação para os handoffs;
- nunca executar deploy, migração ou alteração de serviços externos como parte automática;
- nunca alterar uma implementação anterior;
- nunca editar ou remover entradas antigas da timeline;
- nunca copiar uma implementação anterior para iniciar outra;
- não executar deploy, migração ou alteração de serviços externos como parte automática da skill;
- não incluir segredos ou credenciais.

## Resultado final

Ao terminar, informe:

- implementação usada ou criada;
- status atual;
- arquivos de handoff criados;
- ordem de aplicação;
- verificações incluídas;
- confirmação de que os arquivos originais e implementações anteriores foram preservados.
