# Contrato dos problemas e limites do fluxo de handoffs

## Objetivo

Definir os problemas que o fluxo de handoffs deve controlar no desenvolvimento assistido por IA. Este documento é um contrato de processo: descreve garantias esperadas, limites conhecidos e critérios para considerar uma melhoria válida.

## 1. Evidência declarada sem garantia independente

O handoff deve registrar comandos, resultados esperados e resultados observados. Essa documentação melhora a auditabilidade, mas não transforma automaticamente o relato em prova.

**Contrato:** toda afirmação de conclusão deve apontar para uma evidência reproduzível, mas o fluxo deve declarar quando a evidência foi apenas registrada, quando foi executada no estado atual e quando foi confirmada por integração ou smoke real.

**Limite:** o handoff não substitui execução independente, revisão humana, CI ou observabilidade de produção.

## 2. Múltiplas fontes de estado ativo

`CURRENT.md`, `SEQUENCE.md` e READMEs não podem declarar tarefas ativas diferentes.

**Contrato:** deve existir uma única tarefa ativa por iniciativa; `CURRENT.md` aponta para ela e o registro correspondente deve estar aberto. Iniciativas diferentes podem ter estados históricos ou planejados, mas não podem competir pelo mesmo estado global sem serem identificadas como independentes.

**Limite:** um único `CURRENT.md` não representa múltiplas iniciativas simultâneas. Quando houver concorrência real, a iniciativa deve possuir um identificador de estado próprio ou deve ser encerrada antes de outra ser ativada.

## 3. Memória somente cronológica

Timelines preservam a ordem dos acontecimentos, mas não são suficientes para recuperar decisões permanentes, riscos ou contratos ainda válidos.

**Contrato:** cada implementação deve declarar decisões permanentes, invariantes, riscos vivos e próxima ação quando esses itens existirem.

**Limite:** o handoff não é uma base semântica completa. Busca por conceitos, conflitos entre decisões e síntese histórica exigem leitura dos documentos ou uma ferramenta de indexação auxiliar.

## 4. Duplicação de regras

`AGENTS.md`, `docs/instruction.md`, a skill e os handoffs têm responsabilidades diferentes, mas podem repetir regras.

**Contrato:** `AGENTS.md` contém princípios curtos, `docs/instruction.md` contém a política oficial, a skill contém o procedimento executável e o handoff contém o estado da tarefa. Regras copiadas entre camadas devem apontar para a fonte oficial.

**Limite:** a separação reduz deriva, mas não impede alterações manuais conflitantes. A validação estrutural deve detectar divergências de estado; revisão continua necessária para divergências de intenção.

## 5. Mistura entre status técnico e status de produto

`verified` significa que a implementação passou pelos critérios definidos; não significa automaticamente que a capacidade está pronta para usuários ou aprovada quanto a qualidade, custo e risco.

**Contrato:** o handoff deve separar status de implementação de maturidade da capacidade quando houver impacto de produto, IA, custo, latência, segurança ou operação.

**Limite:** o fluxo de handoffs não decide sozinho se uma capacidade deve ser lançada, mantida ou descontinuada.

## 6. Risco de burocratização

O mesmo ritual aplicado a toda alteração reduz velocidade e incentiva registros artificiais.

**Contrato:** o nível de registro deve ser proporcional ao risco e ao tamanho da mudança. Tarefas pequenas usam um handoff enxuto; tarefas médias usam uma versão completa; tarefas grandes usam sequência, dependências, cobertura e gates explícitos.

**Limite:** uma tarefa classificada como pequena pode crescer durante a execução. Nesse caso, deve ser promovida para `normal` ou `large` sem apagar o histórico já registrado.

## 7. Decisões humanas pouco registradas

Operações e testes não capturam sozinhos as escolhas de engenharia e produto.

**Contrato:** decisões relevantes devem registrar motivo, alternativas consideradas, risco aceito, condição de revisão e impacto esperado.

**Limite:** o agente não deve inventar decisões não fornecidas pelo responsável. Quando a escolha depender de uma decisão humana ausente, deve registrar a pendência em vez de inferir autorização.

## Critério geral de aceitação

O fluxo atende este contrato quando permite responder, sem reconstruir toda a conversa, às perguntas: o que está ativo, por que foi feito, o que mudou, como foi verificado, o que permanece arriscado e qual é o próximo passo proporcional ao tamanho da tarefa.
