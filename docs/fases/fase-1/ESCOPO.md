# Rastro AI — Escopo da Fase 1

## 1. Objetivo

Construir uma demonstração funcional e confiável de um fluxo de IA aplicado à memória de decisões.

Ao final da Fase 1, uma pessoa deve conseguir enviar uma transcrição ou anotação de reunião, fazer perguntas sobre o conteúdo e receber respostas fundamentadas em fontes, com custo, autorização, observabilidade e avaliação reproduzíveis.

O objetivo principal não é entregar um produto corporativo completo. É demonstrar excelência nos fundamentos de engenharia de IA:

- RAG com citações;
- orquestração explícita com LangGraph;
- componentes LangChain dentro dos nós;
- uso controlado de tools;
- avaliação automatizada;
- observabilidade ponta a ponta;
- tratamento de ausência de evidência;
- autorização mínima por projeto;
- métricas de custo por execução.

Evaluation é requisito de primeira classe da Fase 1. O agente não será considerado demonstrável apenas porque responde bem manualmente: suas respostas, retrieval, citações e trajetória precisam ser medidas de forma reproduzível com DeepEval.

## 2. Fluxo principal

```text
upload de transcrição
  ↓
indexação assíncrona
  ↓
pergunta do usuário
  ↓
recuperação de contexto
  ↓
resposta com citações
  ↓
validação das citações
  ↓
trace, custo e evaluation
```

## 3. Exemplo de demonstração

O usuário envia uma transcrição contendo uma discussão sobre arquitetura.

### Pergunta

> Por que a equipe escolheu PostgreSQL?

### Resposta esperada

A resposta deve:

- explicar a decisão;
- mencionar a justificativa encontrada;
- informar, quando disponível, participantes e data;
- citar o documento e o trecho utilizado;
- declarar que não encontrou evidência quando a fonte não sustentar a resposta.

### Resultado esperado

A resposta deve conter a justificativa encontrada, o documento e o trecho usado. Quando não houver evidência suficiente, o agente deve declarar isso sem inventar uma resposta.

## 4. Escopo funcional

### Incluído

- upload de arquivos `.md` e `.txt`;
- cadastro do documento e status de indexação;
- extração de texto;
- divisão em chunks;
- geração de embeddings;
- armazenamento vetorial com PostgreSQL e `pgvector`;
- chat sobre documentos indexados;
- respostas com citações;
- indicação de ausência de evidência;
- histórico básico de conversas;
- feedback positivo ou negativo sobre respostas;
- autorização mínima por organização, projeto, documento e tool;
- escopos propagados do NestJS para o Python por contexto assinado;
- custo estimado por execução, conversa, usuário e projeto;
- tool `search_decisions` para buscar decisões;
- tool `get_document_excerpt` para recuperar trechos de documentos;
- MCP expondo exatamente essas duas tools de leitura;
- traces e métricas no Langfuse;
- dataset de avaliação executado no CI.

### Fora do escopo

Os seguintes itens não fazem parte da implementação da Fase 1:

- autenticação completa, login social e gestão corporativa de identidades;
- multi-tenancy;
- integração com Slack, Teams ou e-mail;
- upload de áudio e transcrição automática;
- suporte inicial a imagens e tabelas complexas;
- múltiplos agentes especializados;
- extração estruturada de decisões e tarefas;
- aprovação humana e execução de alterações;
- muitas tools de escrita;
- vector database dedicado;
- reranking sofisticado;
- dashboard corporativo;
- Kubernetes;
- OAuth completo para clientes MCP externos.

A autorização mínima para separar usuários, projetos, documentos e tools faz parte da Fase 1. A autenticação pode ser simplificada para a demonstração.

Esses itens podem ser documentados como evolução futura, mas não devem atrasar o fluxo principal.

## 5. Arquitetura da Fase 1

```text
rastro-web
    ↓
rastro-api — NestJS
    ├── documentos
    ├── conversas
    └── jobs de indexação
            ↓
rastro-ai — Python
    ├── LangGraph
    ├── LangChain
    ├── RAG
    ├── tools
    ├── worker de indexação
    ├── Langfuse
    └── MCP
```

O `rastro-ai` pode usar a mesma imagem Docker para a API do agente, o worker de indexação e o servidor MCP, com comandos de inicialização diferentes.

## 6. Grafo do agente

O primeiro grafo deve ser pequeno e explícito:

```text
START
  ↓
retrieve_context
  ↓
generate_answer
  ↓
validate_citations
  ↓
END
```

### Responsabilidade dos nós

- `retrieve_context`: busca chunks relevantes no vector store;
- `generate_answer`: responde usando apenas o contexto fornecido;
- `validate_citations`: verifica se as fontes apresentadas existem no contexto recuperado.

O estado do grafo deve conter a pergunta, mensagens, documentos recuperados, resultado das tools, resposta e resultado da validação de citações.

## 7. Evaluation

O dataset inicial deve conter entre 20 e 30 casos, divididos em:

- perguntas respondíveis diretamente;
- perguntas que exigem múltiplos trechos;
- perguntas sem evidência;
- documentos com informações conflitantes;
- tentativas de induzir o modelo a ignorar as fontes;
- casos de seleção de tools.

O DeepEval será executado localmente e no CI. Os datasets e configurações críticas devem permanecer versionados no repositório. O Confident AI não é necessário para concluir esta fase e ficará para a Fase 2 como camada colaborativa de monitoramento e gestão de qualidade em produção.

### Métricas mínimas

- relevância do contexto recuperado;
- contextual precision e recall, quando houver resposta esperada;
- faithfulness;
- relevância da resposta;
- correção das citações;
- escolha correta da tool;
- validação correta das citações.

### Critério de evolução

O objetivo inicial não é atingir uma nota arbitrária. Primeiro deve ser criado um baseline reproduzível. Toda mudança em modelo, prompt, chunking, embeddings, retriever ou grafo deve ser comparada com esse baseline.

O CI deve falhar quando houver regressão relevante nas métricas ou quebra de contratos estruturados.

### Estrutura esperada

```text
evals/
├── dataset.json
├── test_retrieval.py
├── test_answers.py
├── test_citations.py
├── test_tools.py
└── README.md
```

Cada caso deve registrar, quando aplicável, a pergunta, documentos esperados, resposta esperada, citações esperadas, trajetória esperada e critérios de aprovação.

## 8. Observabilidade mínima

Cada pergunta deve produzir um trace contendo:

- `request_id`;
- `conversation_id`;
- `agent_run_id`;
- versão do grafo;
- versão do prompt;
- modelo utilizado;
- chunks recuperados;
- chamadas de tools;
- tokens e custo;
- latência por etapa;
- resposta final;
- feedback do usuário.

O conteúdo deve ser mascarado quando contiver dados pessoais ou informações privadas.

## 9. Critérios de aceite

A Fase 1 estará concluída quando:

- um documento `.md` ou `.txt` puder ser enviado pela interface;
- o usuário conseguir acompanhar o status da indexação;
- uma pergunta puder ser respondida usando o documento indexado;
- a resposta apresentar citações verificáveis;
- o agente disser que não encontrou evidência quando apropriado;
- o fluxo completo aparecer no Langfuse;
- o conjunto de avaliações rodar no CI;
- o DeepEval detectar uma regressão intencional;
- existir um baseline de métricas documentado;
- usuários de projetos diferentes não conseguirem recuperar os documentos uns dos outros;
- uma tool não autorizada ser bloqueada pela API, mesmo quando solicitada pelo modelo;
- o trace mostrar tokens, custo estimado, usuário, projeto e versão do agente;
- existir um teste reproduzível de acesso negado e de orçamento excedido;
- uma tool puder ser chamada pelo agente;
- um cliente MCP puder executar `search_decisions` e `get_document_excerpt` com autorização;
- o projeto puder ser executado localmente com instruções documentadas.

## 10. Roteiro de demonstração

1. Abrir a aplicação.
2. Enviar uma transcrição de reunião.
3. Mostrar a indexação assíncrona.
4. Fazer uma pergunta cuja resposta esteja explícita no documento.
5. Mostrar a resposta e as citações.
6. Fazer uma pergunta sem evidência e mostrar a recusa fundamentada.
7. Mostrar a tool call e a execução do LangGraph.
8. Abrir o trace no Langfuse e verificar custo.
9. Executar a suíte de evaluation.
10. Consultar uma decisão e recuperar seu trecho de origem pelo MCP Inspector ou outro cliente MCP.

## 11. Evolução após a Fase 1

Depois que o fluxo principal estiver estável, as próximas evoluções podem ser:

### Fase 2

- PDF e áudio;
- integração com Slack ou Teams;
- busca híbrida;
- reranking;
- permissões avançadas por projeto e documento;
- extração de decisões e tarefas;
- mais tools de escrita com autorização;
- melhoria do dataset de avaliação;
- revisão colaborativa.

### Fase 3

- multi-tenancy;
- OAuth para MCP;
- memória de longo prazo;
- detecção de decisões contraditórias;
- notificações de tarefas;
- deploy canário de prompts e modelos;
- SLOs de qualidade, custo e latência;
- escala independente do runtime e dos workers.

## 12. Resultado esperado

Ao final da Fase 1, o Rastro não precisa ser um sistema completo de gestão de conhecimento. Ele precisa ser uma demonstração convincente de um agente de IA confiável:

```text
documento real
  → retrieval verificável
  → resposta fundamentada
  → tool controlada
  → trace observável
  → avaliação reproduzível
```

Esse fluxo é o principal artefato técnico da fase e deve receber mais atenção do que a quantidade de telas ou integrações.
