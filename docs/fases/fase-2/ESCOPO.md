# Rastro AI — Fase 2: Qualidade contínua com Confident AI

## 1. Objetivo

Adicionar um ciclo contínuo de avaliação e melhoria da qualidade do agente em produção usando Confident AI, sem substituir o Langfuse utilizado para observabilidade técnica e controle de custos.

```text
Fase 1
  DeepEval local/CI + Langfuse em produção

Fase 2
  DeepEval + Confident AI para qualidade contínua
  Langfuse para traces técnicos e custos
```

## 2. Papel de cada ferramenta

### DeepEval

Biblioteca Python executada no desenvolvimento e no CI.

- define métricas;
- executa testes;
- valida regressões;
- avalia RAG, agentes, tools e trajetórias;
- impede que uma alteração ruim seja publicada.

### Confident AI

Plataforma de qualidade e avaliação em equipe.

- armazena datasets compartilhados;
- compara versões de prompts, modelos e grafos;
- permite revisão humana;
- monitora qualidade de traces em produção;
- agrupa falhas por padrão;
- transforma falhas reais em novos casos de teste;
- fornece alertas de degradação de qualidade.

### Langfuse

Plataforma principal de observabilidade técnica.

- traces de execução;
- latência;
- tokens;
- custo por modelo e feature;
- prompts e versões;
- chunks recuperados;
- chamadas de tools;
- falhas de infraestrutura.

O Confident AI não será usado como substituto do controle de custo e da observabilidade técnica do Langfuse.

## 3. Fluxo da Fase 2

```text
execução em produção
        ↓
trace do agente
        ├── Langfuse: custo, tokens, latência e execução
        └── Confident AI: qualidade e avaliação
                    ↓
              falha detectada
                    ↓
              revisão humana
                    ↓
             novo golden/dataset
                    ↓
              DeepEval no CI
                    ↓
              novo deploy seguro
```

## 4. Funcionalidades incluídas

- conexão do DeepEval com o projeto Confident AI;
- publicação dos datasets principais;
- comparação de versões do modelo;
- comparação de versões de prompt;
- avaliação de trajetória do LangGraph;
- avaliação individual de retriever, generator e tools;
- anotação manual de respostas;
- criação de goldens a partir de falhas reais;
- monitoramento de qualidade em produção;
- alertas para queda de faithfulness, relevância ou correção de citações;
- execução oficial de uma versão de referência;
- sincronização controlada entre datasets remotos e arquivos do repositório.

## 5. Métricas prioritárias

### Respostas

- faithfulness;
- answer relevancy;
- correção das citações;
- taxa de respostas sem evidência;
- aderência ao formato estruturado.

### Retrieval

- contextual relevancy;
- contextual precision;
- contextual recall;
- cobertura das fontes esperadas.

### Agente

- tool selection;
- tool correctness;
- trajetória esperada;
- uso excessivo de tools;
- número de passos;
- falha em solicitar aprovação humana.

### Segurança

- resistência a prompt injection em documentos;
- vazamento de dados privados;
- execução indevida de tools;
- resposta a instruções conflitantes dentro das fontes.

## 6. Critério para promover um caso de produção

Uma falha observada em produção deve seguir este processo:

1. identificar o `agent_run_id` no Langfuse;
2. localizar o trace correspondente no Confident AI;
3. classificar a falha;
4. revisar o caso com uma pessoa;
5. corrigir prompt, retrieval, tool ou código;
6. transformar o caso em golden;
7. adicionar o golden ao dataset;
8. executar DeepEval localmente;
9. publicar uma nova execução oficial;
10. aprovar o deploy somente se não houver regressão importante.

## 7. Limites da integração

Para evitar duplicação e exposição desnecessária de dados:

- não enviar para o Confident AI todos os campos brutos do sistema;
- remover ou mascarar PII antes do envio;
- enviar apenas traces e spans necessários para avaliação;
- manter custo e tokens como fonte principal no Langfuse;
- manter os testes críticos também versionados no Git;
- não depender exclusivamente de um dataset remoto;
- não permitir que a plataforma substitua revisão técnica do código.

## 8. Critérios de aceite

A Fase 2 estará concluída quando:

- o DeepEval publicar avaliações no Confident AI;
- existir um dataset compartilhado com casos do Rastro;
- houver uma versão oficial de referência;
- for possível comparar duas versões do agente;
- um trace de produção puder ser revisado;
- uma falha de produção puder virar um novo golden;
- o CI bloquear uma regressão intencional;
- existir pelo menos um alerta de qualidade;
- Langfuse continuar exibindo custo e tokens;
- dados sensíveis forem mascarados antes do envio.

## 9. Demonstração da Fase 2

1. Executar a versão atual do agente contra o dataset.
2. Publicar a execução como baseline.
3. Alterar o prompt para introduzir uma regressão controlada.
4. Executar novamente as avaliações.
5. Mostrar a queda de faithfulness ou correção de citações.
6. Abrir o trace que causou a falha.
7. Anotar e classificar o problema.
8. Transformar o caso em golden.
9. Corrigir o agente.
10. Executar o CI e demonstrar a recuperação da métrica.
11. Mostrar no Langfuse o custo das duas versões.

## 10. Resultado esperado

Ao final da Fase 2, o Rastro deverá demonstrar não apenas que consegue gerar respostas, mas que consegue operar um ciclo de qualidade:

```text
medir → encontrar falha → revisar → transformar em teste → corrigir → comparar → publicar
```

Essa fase mostra a diferença entre criar uma demo de IA e operar um sistema de IA que melhora com o uso.
