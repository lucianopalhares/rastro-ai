# Rastro AI — Arquitetura

## 1. Visão geral

O Rastro é uma aplicação para transformar conversas, atas, transcrições e documentos em uma memória pesquisável de decisões, justificativas, responsáveis e tarefas.

A arquitetura separa a interface, o domínio da aplicação e o runtime de IA:

```text
Frontend
   ↓
NestJS API
   ├── PostgreSQL
   ├── Object Storage
   ├── Redis ou fila
   └── chama o AI Runtime
             ↓
       Python AI Runtime
          ├── LangGraph
          ├── LangChain
          ├── RAG
          ├── tools
          ├── Langfuse
          └── MCP
```

Essa divisão permite evoluir a aplicação tradicional e a camada de IA em ritmos diferentes, sem transformar cada parte em um microserviço independente desde o início.

## 2. Aplicações

### `rastro-web`

Interface do usuário. Responsabilidades:

- upload de documentos;
- chat;
- exibição de respostas e fontes;
- envio de feedback sobre respostas.

O frontend não chama o modelo diretamente. Toda comunicação passa pela API principal.

### `rastro-api`

API principal em NestJS. É a dona do domínio do produto e das interfaces públicas.

Responsabilidades:

- autenticação e autorização;
- usuários, organizações e permissões;
- documentos e metadados;
- conversas e mensagens;
- armazenamento dos arquivos;
- contratos HTTP públicos;
- criação de jobs de indexação;
- comunicação com o serviço Python de IA.

O NestJS não deve conter prompts, lógica de RAG ou decisões específicas do agente.

### `rastro-ai`

Serviço Python responsável pela inteligência da aplicação.

Responsabilidades:

- execução dos grafos LangGraph;
- componentes LangChain;
- chamadas ao modelo;
- recuperação de contexto;
- tools do agente;
- indexação de documentos;
- embeddings e busca vetorial;
- observabilidade com Langfuse;
- servidor MCP;
- execução das avaliações automatizadas.

Inicialmente, o runtime HTTP, o worker de indexação e o servidor MCP podem usar o mesmo código e a mesma imagem, com comandos de inicialização diferentes:

```text
rastro-ai api
rastro-ai worker
rastro-ai mcp
```

Não é necessário criar três projetos Python separados.

## 3. Ownership dos dados

O NestJS deve ser o dono dos dados de negócio:

- usuários;
- documentos;
- conversas;
- metadados de projetos e documentos;
- permissões.

O serviço Python pode manter artefatos específicos de IA:

- chunks indexados;
- embeddings;
- versões de indexação;
- checkpoints do agente;
- metadados de retrieval.

O Python não deve acessar diretamente as tabelas de negócio do NestJS. Quando precisar consultar dados do produto, deve chamar uma API interna do NestJS. Nesta fase, o agente não altera dados de negócio.

## 4. LangGraph e LangChain

O LangGraph será responsável por orquestrar o fluxo. O LangChain será usado dentro dos nós para fornecer modelos, prompts, retrievers, tools e parsers.

Fluxo inicial do agente:

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

Exemplos de responsabilidades por nó:

- `retrieve_context`: busca os trechos relevantes;
- `generate_answer`: produz uma resposta fundamentada e com citações;
- `validate_citations`: confirma que as fontes apresentadas existem no contexto recuperado.

O estado do LangGraph deve armazenar dados estruturados e brutos, como pergunta, mensagens, documentos recuperados, resultados de tools e resposta. Templates de prompt devem ser montados dentro dos nós, não persistidos no estado.

## 5. RAG

O RAG terá duas etapas distintas.

### Indexação

A indexação acontece quando um documento é enviado:

```text
Upload
  ↓
NestJS salva arquivo e metadados
  ↓
cria job de indexação
  ↓
worker Python
  ├── extrai texto
  ├── divide em chunks
  ├── gera embeddings
  └── salva chunks e vetores
```

Essa etapa deve ser assíncrona para não manter a requisição HTTP aberta durante o processamento.

### Recuperação

A recuperação acontece durante uma pergunta:

```text
Pergunta
  ↓
embedding da pergunta
  ↓
busca vetorial e, futuramente, híbrida
  ↓
chunks relevantes
  ↓
nó de resposta do LangGraph
```

Para a primeira versão, PostgreSQL com `pgvector` reduz a quantidade de infraestrutura. Um vector store dedicado pode ser adotado posteriormente caso volume, latência ou isolamento exijam.

## 6. Tools e MCP

As tools internas do agente devem chamar serviços bem definidos:

```text
search_decisions(query)
get_document_excerpt(document_id)
```

Na Fase 1, o MCP será uma interface adicional, somente leitura, para expor essas duas capacidades a clientes externos, como outros agentes, IDEs ou aplicações compatíveis.

```text
Agente interno ───────┐
                      ├── serviços da aplicação ── API/banco
Cliente MCP externo ──┘
```

As tools do LangGraph e as tools MCP devem reutilizar os mesmos serviços. Não se deve duplicar a lógica de negócio em cada adaptador.

O endpoint MCP precisa de autenticação. A primeira versão deve expor apenas operações de leitura:

- `search_decisions`;
- `get_document_excerpt`;

Não haverá tools MCP de escrita na Fase 1. Operações internas de alteração, como `create_action_item` ou `update_decision`, devem exigir autorização e, quando necessário, confirmação humana.

## 7. Observabilidade

O Langfuse será usado durante as execuções reais do agente para registrar:

- pergunta e resposta;
- modelo e versão;
- prompt utilizado;
- documentos recuperados;
- chamadas de tools;
- tokens e custo;
- latência por etapa;
- erros e retries;
- feedback do usuário.

Cada execução deve possuir identificadores correlacionáveis:

```text
request_id
conversation_id
agent_run_id
document_id
tool_call_id
```

OpenTelemetry deve ser usado para correlacionar traces do frontend, NestJS, fila, Python, banco e chamadas ao modelo. Conteúdo sensível e dados pessoais devem ser mascarados antes de serem enviados para observabilidade.

### Custo por execução

O serviço Python deve registrar no trace o modelo, tokens de entrada e saída, custo estimado, latência, quantidade de chamadas ao modelo e ferramentas utilizadas.

```json
{
  "agent_run_id": "run-123",
  "model": "modelo-versionado",
  "input_tokens": 2840,
  "output_tokens": 620,
  "tool_calls": 1,
  "latency_ms": 4820,
  "estimated_cost_usd": 0.0124
}
```

O custo deve ser calculado a partir do uso retornado pelo provedor e de uma tabela de preços versionada. O valor deve ser associado a usuário, organização, projeto, conversa e versão do agente.

### Autorização por recurso

O NestJS é responsável por autenticar o usuário e autorizar acesso a organizações, projetos, documentos e tools. O Python recebe um contexto assinado e de curta duração com `user_id`, `organization_id`, `project_ids`, roles e scopes.

O retrieval deve filtrar `organization_id`, `project_id` e permissões antes da busca vetorial. Toda tool deve validar seus scopes, e toda operação de escrita deve ser autorizada novamente pela API e exigir confirmação humana quando aplicável. O MCP deve receber credenciais e scopes próprios.

## 8. Evaluation

Evaluation será uma preocupação separada do fluxo normal de produção.

O DeepEval deve rodar no desenvolvimento e no CI usando um dataset versionado:

```text
evals/
├── dataset.json
├── test_retrieval.py
├── test_answers.py
├── test_citations.py
└── test_tools.py
```

Avaliações iniciais:

- relevância do contexto recuperado;
- faithfulness da resposta em relação às fontes;
- relevância da resposta;
- correção das citações;
- escolha correta de tools;
- comportamento quando não existe evidência suficiente.

O dataset deve conter exemplos reais anonimizados, perguntas ambíguas, documentos conflitantes, ausência de informação e tentativas de induzir o agente a ignorar as fontes.

Langfuse pode armazenar traces e scores das execuções reais. DeepEval deve impedir regressões no CI antes de uma nova versão ser publicada.

## 9. Comunicação entre serviços

### Pergunta do usuário

```text
Frontend
  ↓
NestJS valida usuário e cria execução
  ↓
Python executa LangGraph
  ├── recupera contexto
  ├── chama tools quando necessário
  ├── registra trace no Langfuse
  └── gera resposta com citações
  ↓
NestJS entrega a resposta ao frontend
```

### Indexação

```text
Frontend envia arquivo
  ↓
NestJS salva arquivo e cria job
  ↓
worker Python processa o documento
  ↓
status de indexação é atualizado
```

Para respostas longas ou processos demorados, usar jobs assíncronos e streaming de eventos. A API deve controlar timeout, retry, idempotência e cancelamento.

## 10. Deploy inicial

Uma primeira implantação pode conter:

```text
web container
api container
ai-api container
ai-worker container
postgres com pgvector
redis ou broker de mensagens
object storage
langfuse Cloud ou self-hosted
```

O `ai-api` e o `ai-worker` podem usar a mesma imagem Docker. A separação em containers permite escalar a API do agente e a indexação de forma independente sem multiplicar a complexidade do código.

## 11. Ordem de implementação

1. Criar o domínio mínimo no NestJS: documentos, projetos e conversas.
2. Criar upload e armazenamento de arquivos.
3. Implementar indexação assíncrona no Python.
4. Implementar retrieval simples.
5. Criar o primeiro grafo LangGraph para responder com citações.
6. Adicionar tracing no Langfuse.
7. Criar dataset e testes DeepEval.
8. Adicionar tools de leitura.
9. Criar o servidor MCP.
10. Como evolução posterior, adicionar tools de escrita com confirmação humana.

## 12. Princípios

- O modelo não é a fonte de verdade; os documentos e dados recuperados são.
- Dados de negócio permanecem sob controle da API principal.
- Tools de leitura e escrita devem ser separadas.
- Toda alteração feita por IA deve ser autorizada e auditável.
- Indexação deve ser assíncrona e idempotente.
- Prompts, modelos e versões do grafo devem ser versionados.
- Toda resposta de produção deve ser rastreável.
- Evaluation deve bloquear regressões relevantes antes do deploy.
- MCP deve ser uma interface de integração, não um atalho para ignorar autenticação.

## Referências técnicas

- [LangGraph e LangChain](https://docs.langchain.com/oss/python/learn)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Langfuse Python SDK e observabilidade](https://langfuse.com/docs/observability/sdk/overview)
- [DeepEval para avaliação de RAG](https://deepeval.com/docs/getting-started-rag)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
