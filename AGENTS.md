# Instruções do projeto Rastro AI

As regras detalhadas do fluxo de implementações estão em [`docs/instruction.md`](docs/instruction.md), que é a fonte oficial. Este arquivo define regras gerais e não deve duplicar ou contradizer a política detalhada.

Leia `docs/instruction.md` antes de qualquer tarefa. Use `docs/fases/` somente como referência de arquitetura e escopo.

## Regra principal

Implemente diretamente código, configuração, testes e documentação nas aplicações reais. Use `handoffs/` somente para registrar o objetivo, a evolução, os arquivos alterados, as verificações e as pendências; não copie código de aplicação para os handoffs.

## Convenção de linguagem do código

Todo código novo deve usar inglês em nomes de classes, métodos, funções, variáveis, propriedades, interfaces, tipos, enums, módulos e arquivos de código. As instruções, explicações, motivos, impactos e verificações dos handoffs devem ser escritas em pt-BR.

Exceções: quando solicitado pelo usuário, a IA pode editar diretamente `.agents/`, `docs/` e `AGENTS.md`.

## Descoberta no repositório

Para perguntas sobre como, onde ou por que um comportamento funciona, use `jg` primeiro; para nomes exatos, strings ou arquivos, use `rg`/busca de arquivos.

## Memória e reconciliação

O código real e os testes são a fonte da verdade sobre o comportamento atual. Os READMEs registram intenção, decisões, escopo, pendências e continuidade; `CURRENT.md` e `SEQUENCE.md` registram estado e ordem; os timelines registram histórico. Ao continuar uma tarefa, compare essas fontes com o código real e classifique divergências antes de agir. Memórias, índices ou grafos gerados servem apenas para localizar informações.

## Aplicações reais

As aplicações reais são a fonte de verdade do código. Os handoffs são somente histórico e controle do trabalho; nunca trate seus arquivos como código executável.

Quando as aplicações forem criadas, mantenha seus caminhos explícitos nesta seção:

- API: `rastro-api`
- Frontend: `rastro-front`
- IA: `rastro-ai`
- Raiz do projeto: `.`

Se o caminho real não estiver definido ou não existir, peça esclarecimento antes de criar um handoff de código.

Antes de entregar qualquer implementação, execute `.agents/hooks/validate-handoffs.sh` passando o `README.md` e o `TIMELINE.md` da implementação e da versão. A validação confirma a estrutura e a existência dos registros, enquanto testes e lint validam o código real.

## Handoffs

Cada implementação usa o formato:

```text
handoffs/
├── CURRENT.md
├── README.md
├── TIMELINE.md
├── SEQUENCE.md
└── NNN-titulo-em-kebab-case/
    ├── README.md
    ├── TIMELINE.md
    ├── v1/
    │   ├── README.md
    │   └── TIMELINE.md
    └── v2/ (quando houver nova rodada na mesma tarefa)
```

`CURRENT.md` contém somente o número da implementação ativa. `SEQUENCE.md` registra a ordem das tarefas de uma iniciativa. O `handoffs/TIMELINE.md` é o histórico global append-only. Cada implementação também deve conter seu próprio `TIMELINE.md`, append-only, registrando o que cada versão (`v1`, `v2`, `vN`) fez, resolveu ou deixou pendente. Cada rodada de geração dentro de uma tarefa deve ser uma nova versão `vN`, sem sobrescrever versões anteriores. Antes de registrar uma nova entrada, confira e realinhe cronologicamente a ordem dos eventos existentes, sem alterar o texto, status ou conteúdo histórico das entradas.

Cada versão contém somente `README.md` e `TIMELINE.md`. Não copie código, configuração, testes ou documentação de aplicação para `handoffs/`; leia e altere os arquivos reais diretamente. A versão anterior serve apenas para identificar o que foi feito e orientar a reconciliação; a aplicação real decide o que já existe.

Sempre que criar ou atualizar o `vN/README.md`, inclua a seção `## Instruções de validação` com os comandos, URLs, ações manuais ou testes necessários para validar a alteração e o resultado esperado de cada verificação. Quando houver requisição HTTP, inclua o comando completo copiável — por exemplo `curl` — com método, URL, headers, payload ou campos multipart e arquivo de entrada.

Além da seção de validação, inclua, nesta ordem, as seções `## O que foi feito` e `## O que muda na aplicação` antes dela. Registre na primeira as operações aplicadas e o problema resolvido; na segunda, o comportamento novo ou preservado, impactos, limites, riscos e itens fora do escopo. Quando não houver mudança de runtime, declare isso explicitamente.

O `README.md` da versão deve registrar os caminhos reais, operações, âncoras, motivo, impacto, dependências, arquivos alterados e verificações. O código permanece exclusivamente na aplicação real.

Antes de cada classe, interface, método, função, contrato ou bloco removido novo ou alterado, use um comentário JSDoc em pt-BR no formato `/** ... */`. O comentário deve explicar o que o elemento faz e por que existe, seguido de um histórico acumulado por versão (`v1`, `v2` etc.) descrevendo cada mudança daquela versão. Para alteração de linha isolada, coloque o comentário acima do método ou bloco ao qual a linha pertence. Em formatos sem comentários, registre a exceção no README da versão.

Detalhes do formato estão em `docs/instruction.md` e `handoffs/README.md`.

## Rodadas e versões dentro da tarefa

Ao continuar a tarefa apontada por `CURRENT.md`, nunca reutilize nem sobrescreva a saída de uma rodada anterior. Localize a maior versão `vN` dentro da pasta da tarefa e crie a próxima (`v1` na primeira rodada versionada). Antes de gerar qualquer trecho, releia o arquivo original na aplicação real, compare-o com o estado descrito na versão anterior e classifique cada item como já aplicado, aplicado parcialmente, divergente ou ausente.

Gere somente a diferença necessária para o estado real encontrado e aplique-a diretamente nos arquivos reais. Se um trecho de uma versão anterior já estiver aplicado, não o repita. Registre no README da nova versão a versão-base comparada, os arquivos conferidos, o estado encontrado, as mudanças feitas e as pendências.

Cada implementação deve conter seu próprio `README.md` e `TIMELINE.md`. Cada versão deve conter somente seu próprio `README.md` e `TIMELINE.md`. Ao criar ou atualizar uma versão, acrescente no timeline a versão, data/hora, status, arquivos reais conferidos, mudanças aplicadas, problema resolvido, pendências e verificação. Não crie arquivos de código dentro de `handoffs/`.

O README consolidado deve manter, quando aplicável, o estado atual, decisões permanentes, invariantes, aprendizados ou riscos e a próxima ação. O README da versão deve registrar o contexto encontrado, itens já aplicados, decisões tomadas, o que não deve ser repetido e riscos conhecidos.

O README da versão também deve conter as seções obrigatórias `## O que foi feito`, `## O que muda na aplicação` e `## Instruções de validação`.

O `README.md` da implementação é um resumo consolidado e curto da tarefa atual, não um relatório técnico separado: deve explicar o objetivo, o estado e a evolução por todas as versões existentes (`v1`, `v2`, `vN`), usando no máximo uma frase resumida para informar o que cada versão fez ou resolveu, além das pendências e da próxima ação. Por isso, ao criar uma nova versão, atualize o mesmo README sem copiar detalhes técnicos dos handoffs.

## Início, continuidade e ordem

A skill `implementation-flow` só pode ser acionada com uma destas frases exatas:

- `skill iniciar tarefa sobre <objetivo>`;
- `skill finalizar tarefa <numero>`.

Discussão não autoriza geração de handoff: antes de criar ou atualizar arquivos, resuma o plano e aguarde confirmação explícita; na dúvida, permaneça em discussão.

Sem essas frases, use a implementação indicada por `handoffs/CURRENT.md` e não crie outra por inferência. Leia o README da tarefa e o código das aplicações reais.

Para uma solicitação grande:

1. divida o objetivo em tarefas pequenas e verificáveis;
2. registre a sequência, dependências e critérios em `SEQUENCE.md`;
3. ative somente a primeira tarefa;
4. detalhe inicialmente apenas a implementação da tarefa ativa e aplique o código diretamente na aplicação real.

Classifique as demais solicitações como `small`, `normal` ou `large`: mudanças `small` são isoladas e usam registro mínimo; `normal` usa uma implementação com `v1`; `large` exige sequência, dependências e avanço controlado por `CURRENT.md`.

Não pule tarefas. A próxima só pode ser ativada após `skill finalizar tarefa <numero>` e status `applied` ou `verified`. Se o usuário pedir uma tarefa posterior antes disso, informe a tarefa bloqueadora e mantenha `CURRENT.md` inalterado.

Uma implementação nova não copia nem altera implementações anteriores. Correções históricas criam uma nova implementação.

## Verificação e status

Status permitidos: `proposed`, `approved`, `applied`, `verified` e `rolled-back`.

O ciclo normal é `proposed` → `applied` → `verified`; `approved` é opcional e representa aprovação formal antes da aplicação.

- `approved`: confirmação do responsável;
- `applied`: confirmação explícita de aplicação dos trechos;
- `verified`: comandos e resultados dos testes registrados;
- aplicação parcial, divergência ou falha: tarefa permanece ativa e não permite avanço.

Antes de continuar uma tarefa, compare as âncoras com o código real. Se houver divergência ou alterações locais não relacionadas, pare e registre a pendência para decisão. Nunca trate um handoff antigo como evidência do estado atual.

Uma tarefa pode ter sido aplicada parcialmente antes do turno atual, inclusive com alterações diferentes ou trechos já presentes no arquivo original. Portanto, antes de criar, recriar ou ajustar um handoff, releia novamente a pasta real da aplicação e o arquivo original; compare o estado encontrado com a proposta, preserve o que já foi aplicado e reconstrua somente o trecho necessário. Se o arquivo já existir, não aplique um `insert` histórico cegamente: reavalie a operação e as âncoras, usando `replace` quando apropriado. Handoffs anteriores são apenas histórico e nunca substituem essa releitura.

Antes de entregar, confira se o README da versão contém arquivo original, aplicação, operação, âncoras, explicação, impacto, dependências e verificação, e se as alterações estão presentes na aplicação real.

Confira também se as três seções obrigatórias estão presentes na ordem definida.

A finalização deve confirmar arquivos reais e handoffs, pendências e divergências, evidências do status, hook estrutural, testes aplicáveis, lista explícita de commit e avanço permitido de `CURRENT.md`.

Confirme também que o `TIMELINE.md` da implementação foi atualizado no final, sem alterar entradas anteriores. O timeline da implementação registra a evolução detalhada entre versões; o `handoffs/TIMELINE.md` mantém somente o resumo global. Se a ordem estiver errada, mova as entradas inteiras para a posição cronológica correta, sem reescrevê-las.

O JSDoc continua obrigatório para classes, interfaces, métodos, funções, contratos e blocos novos, alterados ou removidos, incluindo finalidade, motivo, principais decisões, comportamento protegido ou alterado e histórico por versão. Elementos puramente mecânicos podem ser explicados no README da versão.

Na finalização, gere o commit automático usando uma lista explícita dos arquivos da própria tarefa, obtida dos handoffs, da aplicação real e dos controles da implementação. Alterações não relacionadas devem permanecer fora do commit e não bloqueiam sua criação; nunca use `git add .` ou `git add -A`. Como `handoffs/` pode estar ignorado por configuração histórica, use `git add -f` somente nos handoffs pertencentes à tarefa. Bloqueie o commit apenas quando houver pendência, versão sem status final, divergência não resolvida ou arquivo da própria tarefa que não possa ser identificado com segurança.

## Limites de segurança

- não execute deploy, migração ou alteração externa como consequência automática;
- não inclua segredos ou credenciais;
- preserve arquivos originais e implementações anteriores;
- alterações de IA devem indicar impacto em qualidade, custo, latência, evaluation e observabilidade quando aplicável.

Para o fluxo completo de iniciar e finalizar tarefas, consulte `.agents/skills/implementation-flow/SKILL.md`.

### `<implementacao>/root/`

Alterações compartilhadas na raiz do projeto, incluindo `.gitignore`, `docker-compose*.yml`, configurações do workspace, scripts de entrada e arquivos que não pertencem exclusivamente à API, ao frontend ou à IA.
