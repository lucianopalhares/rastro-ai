# Rastro AI — Estratégia de Evaluation da Fase 1

## 1. Objetivo

Avaliar a qualidade do agente de forma reproduzível antes e depois de mudanças relacionadas à IA, sem executar o dataset completo em todas as requisições de produção.

Evaluation não será tratado apenas como uma etapa manual de desenvolvimento. A Fase 1 terá:

1. evaluation de regressão no CI;
2. smoke evaluation após deploy;
3. monitoramento online amostrado em produção.

```text
mudança de IA
      ↓
evaluation completo no CI
      ↓
deploy
      ↓
smoke evaluation
      ↓
monitoramento amostrado em produção
```

## 2. Quando executar cada avaliação

### 2.1 Evaluation de regressão

O dataset completo deve ser executado quando houver alteração em qualquer parte que possa modificar o comportamento do agente:

- prompt;
- modelo;
- temperatura ou parâmetros;
- grafo LangGraph;
- tools;
- seleção ou descrição de tools;
- estratégia de RAG;
- chunking;
- embeddings;
- reranking;
- formato de saída;
- memória ou estado do agente;
- código que monta o contexto;
- dependências relevantes de IA.

O resultado deve ser comparado com um baseline versionado. O CI deve bloquear o deploy quando houver regressão relevante ou quebra de contrato estruturado.

### 2.2 Smoke evaluation

Após cada deploy, executar um conjunto pequeno de casos críticos para verificar se o ambiente publicado está operacional.

Casos mínimos:

- pergunta com resposta conhecida;
- retrieval de um documento esperado;
- presença de citação;
- resposta sem evidência;
- chamada de uma tool;
- retorno no schema esperado.

O smoke evaluation não substitui o dataset completo. Ele valida rapidamente a integração entre API, serviço Python, modelo, vector store e tools.

### 2.3 Monitoramento online

O monitoramento online não deve bloquear a resposta do usuário nem executar o dataset completo a cada requisição.

Uma política inicial:

```text
100% das requisições:
  schema, autorização, erros, latência e custo

10% das requisições:
  faithfulness, relevância e qualidade da resposta
```

A avaliação online deve ser assíncrona:

```text
resposta entregue
      ↓
trace no Langfuse
      ↓
job de evaluation
      ↓
worker DeepEval
      ↓
scores e alertas
```

O percentual de amostragem deve ser configurável por ambiente, feature, usuário ou versão do agente.

## 3. Por que monitorar sem mudança de código

Mesmo sem alterar o repositório, a qualidade pode mudar por causa de:

- atualização do modelo pelo provedor;
- mudança de documentos indexados;
- perguntas novas dos usuários;
- degradação do retrieval;
- falhas em tools ou integrações;
- crescimento do contexto;
- mudança de comportamento dos usuários;
- alterações de preço ou limites do provedor.

Por isso, o evaluation de regressão é acionado por mudanças, enquanto o monitoramento online verifica o comportamento real do sistema.

## 4. Dataset da Fase 1

O dataset deve conter entre 20 e 30 casos e permanecer versionado no repositório.

Categorias mínimas:

- perguntas respondíveis diretamente;
- perguntas que exigem múltiplos trechos;
- perguntas sem evidência;
- documentos com informações conflitantes;
- seleção correta entre `search_decisions` e `get_document_excerpt`;
- resposta com citações verificáveis;
- tentativa de prompt injection em documento.

Exemplo de caso:

```json
{
  "id": "decision-001",
  "input": "Por que a equipe escolheu PostgreSQL?",
  "expected_output": "A equipe escolheu PostgreSQL por causa da necessidade de transações relacionais.",
  "expected_sources": ["meeting-architecture-001"],
  "expected_tools": [],
  "category": "grounded_answer"
}
```

Goldens devem ser independentes de uma execução específica. A resposta atual do sistema é gerada durante o teste e comparada com o comportamento esperado.

## 5. Métricas

### Retrieval

- contextual relevancy;
- contextual precision;
- contextual recall;
- presença da fonte esperada.

### Resposta

- faithfulness;
- answer relevancy;
- correção das citações;
- taxa de resposta sem evidência;
- aderência ao tom e formato esperado.

### Agente

- tool selection;
- tool correctness;
- trajetória do LangGraph;
- número de passos;
- validação correta das citações;
- ausência de chamada de tool não autorizada.

### Determinísticas

Executadas sem LLM-as-a-judge, sempre que possível:

- citação aponta para documento existente;
- tool pertence à lista permitida;
- campos obrigatórios presentes;
- limite de passos respeitado;
- custo e tokens registrados.

### Segurança e custo

Além das métricas de qualidade, a Fase 1 deve validar:

- filtro de retrieval por organização e projeto;
- bloqueio de documento fora do escopo do usuário;
- bloqueio de tool sem scope;
- nenhuma escrita de negócio é executada na Fase 1;
- presença de tokens e custo no trace;
- bloqueio ou alerta quando o orçamento da execução for excedido;
- correlação do custo com `user_id`, `project_id` e `agent_version`.

Exemplo de cenário obrigatório:

```text
Usuário do projeto A pergunta sobre o projeto B
→ o filtro impede o acesso aos chunks do projeto B
→ nenhuma tool não autorizada é executada
→ o trace registra a negativa e o custo da tentativa
```

## 6. Organização dos testes

```text
evals/
├── dataset.json
├── baseline.json
├── test_retrieval.py
├── test_answers.py
├── test_citations.py
├── test_tools.py
├── smoke.py
├── replay_production.py
└── README.md
```

### `test_*.py`

Executam o dataset completo no CI usando DeepEval.

### `baseline.json`

Registra a versão do modelo, prompt, grafo, retriever e scores de referência.

### `smoke.py`

Executa os casos críticos depois do deploy.

### `replay_production.py`

Reexecuta traces ou casos selecionados para investigar falhas e validar correções.

## 7. Gates do CI

O CI deve falhar quando ocorrer uma destas situações:

- quebra de schema;
- falha de um teste determinístico crítico;
- tool incorreta ou não autorizada;
- ausência de citação em uma resposta que exige fonte;
- regressão acima do limite definido no baseline;
- aumento de custo acima do orçamento definido;
- aumento de latência acima do limite definido.

Os limites devem ser documentados por métrica. Não se deve comparar scores de execuções feitas com modelos ou modos de avaliação diferentes sem registrar essa diferença.

## 8. Langfuse e DeepEval

### DeepEval

Responsável por executar os testes e calcular métricas no desenvolvimento, no CI e no worker de avaliação online.

### Langfuse

Responsável por registrar:

- traces;
- gerações;
- prompts e versões;
- documentos recuperados;
- tools;
- scores;
- feedback humano;
- custo e tokens.

Scores produzidos pelo DeepEval podem ser associados ao trace correspondente no Langfuse usando `trace_id`, `agent_run_id` ou outro identificador de correlação.

## 9. Feedback humano

A interface deve permitir que o usuário avalie uma resposta:

- útil;
- incorreta;
- sem fonte suficiente;
- fonte inadequada.

O feedback deve ser enviado ao Langfuse e armazenar o identificador do trace. Na Fase 1, esses casos podem ser revisados manualmente e adicionados ao dataset por pull request.

Na Fase 2, o Confident AI poderá automatizar a gestão desses casos, a anotação colaborativa e a promoção de falhas de produção para novos goldens.

## 10. Critérios de aceite

A estratégia de evaluation da Fase 1 estará implementada quando:

- DeepEval executar o dataset no CI;
- houver baseline documentado;
- uma regressão intencional bloquear o CI;
- smoke evaluation rodar após o deploy;
- traces de produção puderem ser avaliados de forma assíncrona;
- pelo menos uma métrica de qualidade for registrada no Langfuse;
- feedback humano estiver associado ao trace;
- o custo da avaliação e da aplicação puder ser identificado;
- casos problemáticos puderem ser reproduzidos por dataset ou replay.

## 11. O que fica para a Fase 2

O Confident AI será adicionado posteriormente para:

- monitoramento contínuo de qualidade em equipe;
- alertas especializados;
- revisão humana colaborativa;
- comparação visual de experimentos;
- agrupamento de falhas;
- gestão remota de datasets;
- promoção automática de traces problemáticos para goldens.

A ausência do Confident AI não impede a conclusão da Fase 1. O fluxo essencial de evaluation será executado com DeepEval, Langfuse, worker assíncrono e datasets versionados no repositório.
