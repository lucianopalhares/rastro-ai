# Handoffs de implementação

As regras oficiais estão em [`../docs/instruction.md`](../docs/instruction.md). Este arquivo resume o formato dos registros; em caso de diferença, a política oficial prevalece.

Esta pasta contém registros das alterações aplicadas diretamente no Rastro AI.

## Memória dos handoffs

Os handoffs formam uma memória em camadas: código real e testes descrevem o comportamento atual; READMEs descrevem intenção, decisões, escopo e pendências; `CURRENT.md` e `SEQUENCE.md` descrevem estado e ordem; timelines descrevem histórico. Em caso de conflito, o código e os testes vencem para o comportamento atual, e o conflito deve ser registrado como pendência.

## Organização

```text
handoffs/
├── CURRENT.md
├── README.md
├── TIMELINE.md
├── SEQUENCE.md
├── 001-nome-da-implementacao/
│   ├── README.md
│   └── v1/
│       ├── README.md
│       └── TIMELINE.md
└── 002-outra-implementacao/
    ├── README.md
    ├── TIMELINE.md
    └── v1/
        ├── README.md
        └── TIMELINE.md
```

Cada pasta numerada representa uma implementação coerente. O código é aplicado diretamente nas aplicações reais; use o próximo número disponível e um título em `kebab-case`.

Uma solicitação grande pode gerar várias implementações numeradas relacionadas. Divida quando houver muitas alterações, mais de uma aplicação, dependências entre etapas, validações diferentes ou um handoff difícil de revisar. Cada implementação deve ter um único objetivo, poucos arquivos relacionados, critério de conclusão próprio e ordem de aplicação explícita. Divida por capacidade verificável, não simplesmente por arquivo.

As etapas devem permanecer isoladas. Uma etapa pode declarar dependência de outra pelo número, mas não deve copiar seus handoffs nem alterar sua pasta. Registre no README da etapa a iniciativa relacionada, dependências, ordem, próxima etapa e critério de conclusão. `CURRENT.md` aponta somente para a etapa ativa.

Quando uma solicitação gerar várias etapas, a IA deve definir primeiro a sequência completa e ativar apenas a primeira. As demais podem ser registradas como planejadas, mas recebem handoffs detalhados somente quando chegarem à vez. Não é permitido pular etapas: a próxima só pode ser ativada após a finalização explícita da atual com `skill finalizar tarefa <numero>` e status `applied` ou `verified`.

Toda implementação deve conter pelo menos uma versão `vN`, e toda versão deve conter somente `README.md` e `TIMELINE.md`. Não copie arquivos de código para esta pasta. Todo README de versão deve conter `## Instruções de validação`, com comandos, URLs, ações ou testes e o resultado esperado. Requisições devem trazer comando completo copiável, como `curl`, com URL, método, payload/campos, arquivo e resposta esperada.

## Rodadas da mesma implementação

Quando a tarefa continuar após uma primeira rodada, crie `v2/`, depois `v3/` e assim por diante dentro da pasta da implementação. Não sobrescreva a versão anterior. Cada versão registra somente mudanças aplicadas diretamente no código real.

Antes de criar uma versão, leia o README da tarefa, o README da versão anterior e, obrigatoriamente, os arquivos originais das aplicações reais. Compare item a item: `aplicado`, `parcial`, `divergente` ou `ausente`. A aplicação real é a única fonte de verdade; a versão anterior só informa o que foi proposto e quais pontos precisam ser conferidos.

A nova versão deve conter somente a diferença ainda necessária. Não repita trechos já presentes no código. Se âncoras ou contexto mudaram, reconstrua o handoff com base no arquivo atual e reavalie `insert`, `replace` ou `remove`. O `README.md` da versão deve registrar versão-base, arquivos conferidos, reconciliação, pendências, ordem e verificações.

Use o formato `NNN-titulo-em-kebab-case` para a pasta da implementação. O caminho original completo e os metadados dos arquivos reais ficam no `README.md` da versão:

```text
handoffs/001-validacao-de-citacoes/v1/README.md
```

O handoff contém somente o registro da mudança e não é código de produção. Para arquivo novo, informe o caminho pretendido e use `insert`. `CURRENT.md` e `TIMELINE.md` ficam na raiz de `handoffs/`, e cada versão possui seu próprio `TIMELINE.md`.

Os arquivos de cada versão são somente registros. A fonte de verdade são as aplicações reais; versões anteriores são históricos e não devem ser usadas para reconstruir o código.

Toda implementação deve conter também um `README.md` próprio, curto e com no máximo 8 linhas de conteúdo. Ele funciona como cartão de contexto; os detalhes técnicos ficam no README e no timeline da versão.

O cartão de contexto deve preservar, quando aplicável, estado atual, decisões permanentes, invariantes, aprendizados ou riscos e próxima ação. A versão deve registrar contexto encontrado, itens já aplicados, decisões tomadas, o que não deve ser repetido e riscos conhecidos.

As regras detalhadas de handoff descritas abaixo aplicam-se às alterações do projeto em geral. Alterações em `.agents/`, `docs/` e `AGENTS.md` podem ser feitas diretamente quando solicitadas e não precisam ser copiadas para esta pasta. O `README.md` da implementação, `CURRENT.md` e `TIMELINE.md` seguem seus formatos compactos de controle.

Consulte [`CURRENT.md`](./CURRENT.md) para identificar a implementação ativa. O arquivo contém somente o número inicial da pasta ativa, com três dígitos. Uma implementação nova começa sempre em uma pasta nova e não deve alterar ou copiar os arquivos de implementações anteriores.

`SEQUENCE.md` registra a ordem central das tarefas de cada iniciativa. Antes de detalhar a primeira tarefa, registre a sequência completa, suas dependências e critérios de avanço.

## Como iniciar uma implementação

O usuário pode escrever, por exemplo:

```text
Inicie uma nova implementação chamada rag-com-citacoes.
```

O agente deve então:

1. identificar o próximo número disponível;
2. criar `handoffs/<numero>-rag-com-citacoes/`;
3. criar `v1/README.md` e `v1/TIMELINE.md`;
4. criar o README da implementação;
5. atualizar `CURRENT.md` com apenas o novo número;
6. adicionar uma entrada ao final de `TIMELINE.md`;
7. aplicar diretamente a mudança na aplicação real e registrar os arquivos alterados no README da versão.

Se a solicitação for uma continuação do objetivo atual, o agente usa a pasta indicada em `CURRENT.md`. Se não for possível distinguir os casos, deve perguntar antes de criar ou alterar arquivos.

Os caminhos absolutos ou relativos dos arquivos reais devem ser informados no README da versão, junto com a operação e a âncora estrutural.

## Índice de implementações

Mantenha aqui uma lista curta das implementações, em ordem numérica, com seu objetivo. O histórico detalhado e cronológico fica em [`TIMELINE.md`](./TIMELINE.md), que deve receber apenas novas entradas ao final.

| Número | Título | Objetivo | Ordem |
| --- | --- | --- | --- |
| `001` | `exemplo-validacao-citacoes` | Exemplo didático de handoff | conforme README da implementação |
| `004` | `upload-minimo-de-arquivos` | Receber, armazenar e associar arquivos `.md` e `.txt` | após `003`, antes de `005` |

## Registro obrigatório

Toda nova implementação deve atualizar `handoffs/TIMELINE.md` com uma entrada de no máximo 8 linhas. A entrada deve conter título, data e hora, status, aplicação afetada, motivo, impacto, o que foi resolvido e a pasta relacionada. Antes da entrega, realinhe apenas a posição das entradas inteiras em ordem cronológica, preservando todo o conteúdo histórico.

Na finalização, o commit deve usar uma lista explícita somente dos arquivos da tarefa. Alterações não relacionadas ficam fora do índice e não bloqueiam o commit; nunca usar `git add .` ou `git add -A`. Se `handoffs/` estiver ignorado, usar `git add -f` apenas nos handoffs da tarefa. Bloquear somente por pendências, divergências, versões sem status final ou arquivos próprios da tarefa não identificáveis.

Não edite entradas antigas. Não altere pastas de implementações finalizadas. Para iniciar uma nova unidade de trabalho, crie a próxima pasta numerada e atualize `CURRENT.md`.

Use somente estes status: `proposed`, `approved`, `applied`, `verified` e `rolled-back`. Alterações de status devem gerar uma nova entrada compacta ao final da `TIMELINE.md` e atualizar o status do README da implementação, sem ultrapassar 8 linhas.

O ciclo normal é `proposed` → `applied` → `verified`. Use `approved` somente para aprovação formal antes da aplicação e `rolled-back` para uma aplicação revertida.

### Classificação de esforço

- `small`: mudança isolada, sem dependências entre etapas e com verificação simples; registra objetivo, arquivos, motivo, impacto e validação sem criar sequência adicional.
- `normal`: capacidade única com implementação numerada e `v1`.
- `large`: várias etapas, aplicações ou dependências; exige `SEQUENCE.md` e controle por `CURRENT.md`.

Formato da timeline e do README de cada implementação. Cada campo após o título deve ser um item de lista Markdown iniciado por `- `:

```markdown
## 001 — Título curto

- Data/hora: 2026-10-23 11:03 -03:00 | Status: `proposed`
- Aplicação afetada: `ia`
- Dependência/ordem: `nenhuma` | Próxima: `002-proxima-etapa`
- Por que foi feito: motivo resumido.
- Impactos: efeito resumido.
- Resolve: problema resolvido. Critério: condição verificável de conclusão.
- Pasta: `handoffs/001-titulo-curto/`
```

O título deve começar pelo número da tarefa e remeter diretamente ao que foi feito. Detalhes, âncoras, código e verificações continuam nos arquivos de handoff.

## Formato obrigatório de cada alteração

Use este formato no README da aplicação ou no cabeçalho do handoff:

```markdown
## Alteração: nome curto

- Arquivo original: `/caminho/absoluto/para/o/arquivo`
- Aplicação: `api`, `front` ou `ia`
- Localização: linha atual, seção/função e âncoras estáveis
- Operação: `insert`, `replace` ou `remove`
- O que o trecho faz: explicação do comportamento do código
- Motivo: por que a alteração é necessária
- Impacto: o que muda no comportamento
- Pré-requisitos: alterações que devem ser aplicadas antes
- Linhas afetadas: linhas após a aplicação, sempre junto da âncora estrutural

### Ponto estrutural

```text
função, classe, método, import, chave de configuração ou seção
...
```

### Explicação do trecho

- O que este código faz: explicação objetiva do comportamento do arquivo e dos blocos relevantes.
- Por que inserir, substituir ou remover: justificativa técnica.
- Comentários no código: usar JSDoc `/** ... */` em pt-BR acima de toda classe, interface, método, função, contrato ou bloco novo, alterado ou removido; explicar finalidade, motivo, principais decisões, comportamento protegido ou alterado e manter histórico acumulado por versão (`v1`, `v2` etc.). Elementos puramente mecânicos podem ser explicados somente no README.
- O que permanece inalterado: limites do trecho aplicado.

### Aplicação e verificação

1. Confirmar que a alteração está aplicada no arquivo real indicado.
2. Executar os testes especificados.
3. Conferir o comportamento esperado.
```

## Regras

- não copiar código para os handoffs;
- não alterar seções vizinhas que não fazem parte da tarefa;
- usar número de linha apenas como referência auxiliar;
- usar trechos anterior e posterior para delimitar cada alteração;
- usar funções, classes, métodos, chaves ou seções como âncoras verificáveis;
- explicar individualmente cada trecho alterado, inserido ou removido;
- explicar a ordem de aplicação;
- incluir testes, evaluation e observabilidade quando a alteração afetar a IA;
- não executar automaticamente o conteúdo do handoff;
- não incluir segredos, tokens ou credenciais.

## Critério de completude

Um handoff está completo quando outra pessoa consegue aplicá-lo sem consultar o raciocínio original, sabendo:

- qual arquivo alterar;
- em qual aplicação ele está;
- onde alterar;
- qual operação executar;
- qual conteúdo copiar;
- por que a mudança existe;
- quais testes executar;
- quais alterações permanecem fora do escopo.

### Checklist de finalização

- [ ] arquivos reais e arquivos do handoff conferidos;
- [ ] pendências e divergências resolvidas ou registradas;
- [ ] status compatível com confirmação ou evidência;
- [ ] hook estrutural e testes aplicáveis executados;
- [ ] lista explícita de commit conferida;
- [ ] `CURRENT.md` avançado somente após `applied` ou `verified`.
