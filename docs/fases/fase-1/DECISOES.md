# Rastro AI — Decisões técnicas

Este documento registra as principais decisões do Rastro AI, seus motivos, trade-offs e possíveis evoluções.

## 1. Separação entre frontend, API e IA

### Decisão

O sistema será dividido em três aplicações:

- `rastro-web`: interface do usuário;
- `rastro-api`: API principal em NestJS;
- `rastro-ai`: serviço Python de IA.

### Motivo

A API principal possui responsabilidades tradicionais de produto, como autenticação, permissões, persistência e contratos HTTP. A camada de IA possui dependências, ciclos de evolução e necessidades operacionais diferentes, como modelos, embeddings, LangGraph, LangChain e avaliação.

Essa separação permite evoluir a IA sem misturar prompts e lógica de agente com as regras do domínio principal.

### Trade-off

Há mais complexidade operacional, principalmente na comunicação entre NestJS e Python, no tratamento de timeouts e na observabilidade distribuída.

### Melhoria possível

Para uma primeira prova de conceito, frontend, API e IA poderiam ser executados juntos. Em produção, a separação deve ser mantida, mas os serviços podem compartilhar pipelines de deploy, configurações e templates de infraestrutura.

## 2. NestJS como dono do domínio do produto

### Decisão

O NestJS será responsável pelos dados e regras do produto:

- usuários e organizações;
- autenticação e autorização;
- documentos;
- conversas;
- projetos e metadados de documentos;
- histórico e auditoria.

### Motivo

Evita que o agente tenha acesso direto e irrestrito ao banco de dados. A API mantém controle de permissões, validações, auditoria e consistência.

### Trade-off

O serviço Python precisa chamar APIs internas para obter ou alterar dados, acrescentando latência e pontos de falha.

### Melhoria possível

Usar contratos versionados, clientes tipados e autenticação serviço-a-serviço. Para operações críticas, adicionar autorização por escopo e idempotency keys.

## 3. Python como runtime de IA

### Decisão

A implementação de IA será feita em Python, usando LangGraph e LangChain.

### Motivo

Python oferece um ecossistema amplo para RAG, embeddings, avaliação, processamento de documentos e experimentação com modelos. Também permite manter a camada de IA independente da linguagem da API principal.

### Trade-off

O time precisa manter duas stacks e lidar com contratos entre TypeScript e Python.

### Melhoria possível

Gerar clientes e schemas a partir de OpenAPI ou JSON Schema, evitando duplicação manual dos contratos.

## 4. LangGraph para orquestração

### Decisão

O LangGraph será responsável pelo fluxo explícito do agente, estado, retries e validação de citações. Pausas para intervenção humana ficam para uma evolução posterior.

### Motivo

O fluxo precisa ser observável e previsível. Separar etapas como classificação, retrieval, escolha de tool e geração da resposta facilita testes, recuperação de falhas e evolução do agente.

### Trade-off

Um grafo explícito exige mais código do que uma chamada simples a um agente pronto. Também é necessário versionar mudanças no estado e nos nós.

### Melhoria possível

Adicionar persistência de checkpoints em banco, políticas de retry por nó, limites de passos, cancelamento e uma estratégia formal de migração de estado entre versões do grafo.

## 5. LangChain dentro dos nós

### Decisão

LangChain será utilizado como biblioteca de componentes dentro dos nós do LangGraph:

- modelos;
- prompts;
- retrievers;
- loaders;
- splitters;
- tools;
- parsers;
- saídas estruturadas.

### Motivo

O LangGraph define o fluxo, enquanto o LangChain fornece componentes reutilizáveis para cada etapa. Isso preserva a separação entre orquestração e implementação dos nós.

### Trade-off

Abstrações demais podem dificultar o diagnóstico de problemas e tornar atualizações de versão mais trabalhosas.

### Melhoria possível

Manter interfaces próprias para `LLM`, `Retriever` e `EmbeddingModel` nas partes críticas. Assim, o domínio não fica diretamente acoplado a uma implementação específica do LangChain.

## 6. RAG separado em indexação e recuperação

### Decisão

O RAG será dividido em dois fluxos:

1. indexação assíncrona quando um documento é enviado;
2. recuperação durante a pergunta do usuário.

### Motivo

Indexar documentos dentro da requisição de upload deixaria a interface lenta e frágil. Separar os fluxos permite reprocessar documentos, acompanhar status e escalar workers independentemente.

### Trade-off

O documento não fica imediatamente disponível e o sistema precisa controlar estados como `pending`, `processing`, `ready` e `failed`.

### Melhoria possível

Adicionar versionamento de índice, reindexação parcial, hash de conteúdo para evitar duplicatas, cache de embeddings e busca híbrida combinando texto e vetores.

## 7. PostgreSQL com pgvector inicialmente

### Decisão

O primeiro vector store será PostgreSQL com `pgvector`, evitando a introdução imediata de um banco vetorial dedicado.

### Motivo

Reduz a infraestrutura necessária para o MVP e facilita backup, desenvolvimento local e operação de uma base pequena ou média.

### Trade-off

Um banco vetorial especializado pode oferecer recursos melhores para grandes volumes, filtros complexos ou cargas de busca mais intensas.

### Melhoria possível

Medir latência, cardinalidade, volume de chunks e custo operacional. Migrar para um vector store dedicado apenas se os dados justificarem a mudança.

## 8. Serviço Python sem acesso direto às tabelas de negócio

### Decisão

O serviço Python não acessará diretamente os dados de domínio mantidos pelo NestJS. Ele utilizará APIs internas para consultar documentos e projetos autorizados.

### Motivo

Isso centraliza autenticação, autorização, validação e auditoria no serviço que possui o domínio.

### Trade-off

Chamadas de rede adicionam latência e podem falhar durante uma execução do agente.

### Melhoria possível

Adicionar timeouts curtos, retries limitados, circuit breaker, cache somente para leituras seguras e contratos internos versionados.

## 9. Tools de leitura antes de tools de escrita

### Decisão

O agente começará com ferramentas de consulta:

- buscar decisões;
- consultar documentos;
- recuperar trechos de fontes.

Alterações de dados exigirão confirmação e autorização.

### Motivo

Operações de leitura têm menor risco e são suficientes para validar a qualidade do agente, do RAG e das citações antes de automatizar ações.

### Trade-off

O MVP terá menos automação e não executará alterações de dados.

### Melhoria possível

Adicionar aprovação humana, escopos por tool, limites de impacto, idempotência, trilha de auditoria e rollback para operações de escrita.

## 10. MCP como interface de integração

### Decisão

O MCP será implementado no serviço Python como uma interface adicional para expor tools e resources a clientes externos.

Na Fase 1, o MCP exporá exatamente duas tools de leitura:

- `search_decisions(query)`;
- `get_document_excerpt(document_id)`.

Não serão expostas tools MCP de escrita nesta fase.

### Motivo

A capacidade do Rastro poderá ser reutilizada por outros agentes, IDEs e aplicações compatíveis sem duplicar toda a lógica do produto.

### Trade-off

MCP adiciona uma superfície de integração que precisa de autenticação, autorização, versionamento e monitoramento.

### Melhoria possível

Começar com transporte local para desenvolvimento e HTTP protegido para produção. Adicionar OAuth, escopos por tool, limites de taxa, validação de argumentos e isolamento de credenciais.

## 11. Langfuse para observabilidade de IA

### Decisão

Langfuse será utilizado para traces, prompts, gerações, retrieval, tool calls, custo, latência e feedback.

### Motivo

Os problemas de uma aplicação de IA normalmente atravessam várias etapas. Registrar somente a resposta final não permite saber se o erro veio do retrieval, do prompt, do modelo ou de uma tool.

### Trade-off

Traces podem conter documentos privados, conversas e dados pessoais. Também há custo e volume de armazenamento.

### Melhoria possível

Aplicar mascaramento de PII, retenção configurável, amostragem de traces, controle de acesso e separação entre ambientes de desenvolvimento, staging e produção.

## 11.1 Custo como métrica operacional

### Decisão

Cada execução deve registrar tokens, custo estimado, modelo, versão do agente, usuário, organização e projeto no Langfuse.

### Motivo

Uma aplicação de IA precisa demonstrar não apenas qualidade, mas também previsibilidade financeira. O custo deve ser calculado a partir do uso real do provedor e de preços versionados.

## 11.2 Autorização mínima na Fase 1

### Decisão

Mesmo sem autenticação completa, a demonstração terá usuários, projetos e scopes mínimos. O NestJS será o dono da autorização; o Python apenas executará o contexto autorizado e as tools permitidas.

### Motivo

Evita que o modelo ou o retrieval acesse documentos de outro projeto. A autorização será aplicada no endpoint, no retrieval, nas tools e no MCP.

## 12. DeepEval para avaliação automatizada

### Decisão

DeepEval será utilizado no CI para testar retrieval, respostas, citações e comportamento das tools.

Essa decisão faz parte da Fase 1 e é obrigatória para o fluxo demonstrável. O Confident AI será introduzido somente na Fase 2, como plataforma compartilhada para monitoramento, revisão humana e gestão de datasets de qualidade.

### Motivo

Testes tradicionais não capturam bem faithfulness, relevância ou qualidade de uma resposta gerada. Um dataset versionado permite detectar regressões após trocar modelo, prompt, chunking ou retriever.

### Trade-off

Avaliações baseadas em LLM podem ser caras, lentas e não totalmente determinísticas. Métricas automáticas também não substituem revisão humana.

### Melhoria possível

Combinar três tipos de avaliação:

1. testes determinísticos, como schema, JSON, citações e seleção de tool;
2. métricas baseadas em LLM, como faithfulness e relevância;
3. revisão humana de uma amostra representativa.

## 13. OpenTelemetry para correlação ponta a ponta

### Decisão

A aplicação usará OpenTelemetry para correlacionar traces entre frontend, NestJS, filas, Python, banco e chamadas ao modelo.

### Motivo

Uma execução pode passar por vários serviços. Um `trace_id` compartilhado torna possível investigar a jornada completa de uma pergunta.

### Trade-off

Instrumentação exige padronização de nomes, atributos, propagação de contexto e cuidado com conteúdo sensível.

### Melhoria possível

Definir convenções próprias para `agent_run_id`, `conversation_id`, `retrieval.query`, `retrieval.documents`, `tool.name`, `model.name`, custo e versão do grafo.

## 14. Jobs assíncronos para indexação

### Decisão

Indexação, reindexação e processamento de documentos serão executados por workers, usando Redis ou um broker de mensagens.

### Motivo

Essas operações podem demorar, falhar por motivos transitórios e exigir retry. O worker evita bloquear a API e permite escalar processamento separadamente.

### Trade-off

Introduz complexidade de estados, filas, retries e idempotência.

### Melhoria possível

Adicionar dead-letter queue, backoff exponencial, métricas de fila, deduplicação de jobs e reprocessamento manual pelo painel administrativo.

## 15. Implantação inicial com containers separados

### Decisão

O deploy inicial terá containers para frontend, API, AI Runtime e worker, além da infraestrutura de dados.

O runtime e o worker podem usar a mesma imagem Python com comandos diferentes.

### Motivo

Permite escalar o agente e a indexação de forma independente sem criar múltiplos projetos ou duplicar código.

### Trade-off

A operação fica mais complexa do que executar uma única aplicação.

### Melhoria possível

Usar uma plataforma gerenciada para filas, banco e observabilidade antes de adotar Kubernetes. Kubernetes só deve ser introduzido quando houver necessidade operacional real.

## 16. O que seria melhorado com mais tempo

### Produto

- integrações com Slack, Microsoft Teams e e-mail;
- importação de áudio com transcrição;
- revisão colaborativa de decisões;
- histórico de decisões substituídas;
- notificações de tarefas e prazos;
- permissões por projeto e documento.

### RAG

- busca híbrida lexical e semântica;
- reranking;
- detecção de documentos conflitantes;
- indexação multimodal de tabelas e imagens;
- filtros por projeto, autor e período;
- avaliação de recall do retriever com dataset curado.

### Agente

- aprovação humana dentro do fluxo LangGraph;
- memória por usuário, organização e projeto;
- classificação de confiança;
- respostas com citações verificadas automaticamente;
- políticas para evitar que instruções dentro de documentos controlem o agente;
- limite de custo e número de chamadas por execução.

### Segurança

- autenticação serviço-a-serviço com rotação de credenciais;
- isolamento por tenant;
- criptografia de arquivos e dados sensíveis;
- redaction de PII nos traces;
- análise de prompt injection em documentos;
- auditoria de todas as tools de escrita;
- política de retenção e exclusão de dados.

### Operação

- deploy canário de prompts e modelos;
- feature flags para versões do grafo;
- rollback de prompts, modelos e índices;
- SLOs para latência e disponibilidade;
- alertas de aumento de custo, erro e queda de qualidade;
- testes de carga do retrieval e do worker.

## 17. Decisão de escopo do MVP

O MVP não terá agentes autônomos complexos nem múltiplos agentes especializados. O primeiro objetivo é validar um único fluxo confiável:

```text
upload de documento
  → indexação
  → pergunta
  → recuperação de contexto
  → resposta com citações
```

Depois que esse fluxo tiver observabilidade e evaluation suficientes, serão adicionadas tools de escrita e novas integrações MCP. Essa ordem reduz risco e permite medir a qualidade de cada camada antes de aumentar a autonomia do sistema.

