# Evaluation da busca semântica

Este módulo verifica se a busca encontrou os chunks certos.

Ele não cria uma resposta com LLM.

## O que é comparado

O golden dataset diz:

```text
Para esta pergunta, estes chunks são os corretos:
meeting-db:0
```

A busca retorna:

```text
1. meeting-cache:0
2. meeting-db:0
3. planning:0
```

O evaluator compara as duas listas e calcula as métricas.

## Existem dois tipos de teste

### 1. Teste automatizado

Este teste usa resultados falsos e controlados. Ele verifica se o código das métricas está calculando corretamente.

Ele não usa:

- PostgreSQL;
- PGVector;
- OpenAI;
- documentos reais.

Execute pelo Docker:

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation
```

Deu certo quando aparecer:

```text
OK
```

Esse resultado significa somente que as métricas estão implementadas corretamente.

### 2. Evaluation real

Esta avaliação usa o caminho real da aplicação:

```text
pergunta
→ embedding real
→ PGVector
→ chunks reais
→ métricas
```

Antes de executar, é necessário que:

1. `evaluation-vector-db` esteja ativo;
2. a coleção de evaluation seja preparada pelo comando abaixo;
3. `OPENAI_API_KEY` esteja configurada.

Execute primeiro a preparação do corpus. Ela lê os `documents` do único golden dataset, usa o chunker real da aplicação e grava os chunks em um container PostgreSQL/PGVector exclusivo da evaluation, com o mesmo schema do banco principal:

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d evaluation-vector-db
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -e DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation -e PGVECTOR_COLLECTION=rastro_document_chunks -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m evals.retrieval.prepare --dataset /app/evals/dataset/golden.json
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -e DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation -e PGVECTOR_COLLECTION=rastro_document_chunks -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m evals.retrieval.evaluate --dataset /app/evals/dataset/golden.json --ks 1,3,5
```

Deu certo tecnicamente quando o comando terminar sem erro e imprimir um JSON com os casos avaliados.

Isso ainda não significa que a qualidade está boa. Para avaliar a qualidade, confira:

- `project_isolation` deve ser `1.0`;
- `score_ordering` deve ser `1.0`;
- `abstention` deve ser `1.0` nos casos sem evidência;
- Recall, Precision, MRR e nDCG devem atingir os limites definidos pelo projeto.

## Diferença em uma frase

```text
Teste automatizado: verifica se o código da avaliação funciona.
Evaluation real: verifica se a busca semântica real funciona bem.
```

O comando real atualmente não reprova sozinho métricas abaixo do limite. A equipe precisa comparar os valores impressos com o baseline ou com os limites definidos para o produto.

### Script curto para executar a evaluation

O script abaixo encapsula os comandos Docker dos dois cenários:

```bash
./run_evaluation.sh test
```

O modo `test` executa os testes automatizados com resultados controlados. Ele não sobe banco, não chama OpenAI e não usa documentos indexados.

Para executar a evaluation real contra o PGVector isolado:

```bash
./run_evaluation.sh real
```

O modo `real` não reindexa o corpus por padrão. Para preparar novamente o banco e depois executar a avaliação:

```bash
./run_evaluation.sh real --prepare
```

Para alterar os valores de `k`:

```bash
./run_evaluation.sh real --ks 1,3,5,10
```

Use `--prepare` somente quando o `golden.json` ou a estratégia de chunking tiver mudado, porque essa opção gera embeddings novamente.

### Estrutura do relatório

O evaluator não envia dados ao Langfuse nesta versão, mas já imprime um contrato organizado para permitir uma integração futura sem refazer os cálculos:

```text
relatório
├── schema
├── run
│   ├── dataset
│   ├── ks
│   └── retriever
├── summary
│   ├── contagens
│   ├── failure_count
│   └── metrics
├── scores
│   └── name, value, data_type
├── quality
│   ├── status
│   ├── thresholds
│   └── checks
├── failures
└── cases
    ├── input
    ├── expected
    ├── retrieval
    ├── scores
    └── diagnostics
```

O campo `quality.status` fica como `not_evaluated` enquanto não houver thresholds configurados. `failures` contém somente os casos que precisam de investigação, com razões como `relevant_chunk_below_top` ou `returned_without_expected_evidence`. `cases` mantém o detalhe completo para uma futura criação de traces e scores no Langfuse.

## Instruções de validação

### Validar o código das métricas

Execute este comando a partir da raiz do projeto. Ele cria um container temporário do `ai-indexer`, monta somente os testes e os evaluators e executa o teste com resultados controlados. Ele não precisa de PostgreSQL, OpenAI ou documentos indexados.

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation
```

O comando foi dividido conceitualmente assim:

- `run --rm`: cria e remove um container somente para a execução;
- `--no-deps`: não inicia banco, porque este teste usa retriever fake;
- `-v ...tests` e `-v ...evals`: disponibiliza testes e código/dataset no container;
- `python -m unittest ...`: executa o teste das métricas.

Resultado esperado: `OK`. Isso prova que o código calcula as métricas corretamente; não prova que o PGVector real está retornando bons chunks.

### Validar a busca semântica real

Primeiro, deixe o PostgreSQL/PGVector e o indexador ativos. Este comando só prepara os serviços:

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d evaluation-vector-db
```

Depois, execute o evaluator. Ele consulta a mesma coleção isolada preparada no passo anterior e chama o `search_relevant_chunks()` real:

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -e DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation -e PGVECTOR_COLLECTION=rastro_document_chunks -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m evals.retrieval.evaluate --dataset /app/evals/dataset/golden.json --ks 1,3,5
```

Antes do comando de preparação, `OPENAI_API_KEY` precisa estar configurada. O `expected_answer` continua no mesmo golden dataset e será usado pelos próximos evaluators de resposta; o retrieval usa `relevant_chunks`, enquanto o corpus usa `documents`. O JSON produzido contém os chunks retornados e as métricas por caso.

Resultado esperado da execução: o comando termina sem traceback e imprime JSON. Resultado esperado da qualidade: `project_isolation` e `score_ordering` iguais a `1.0`, abstinência correta nos casos sem evidência e as métricas de ranking acima dos thresholds do projeto. O CLI ainda não reprova automaticamente thresholds; essa comparação é manual nesta versão.

### Depurar a avaliação real no VS Code

O comando normal acima executa `evaluate.py`, mas não inicia um debugger. Por isso um breakpoint no arquivo não será acionado. Para depurar, substitua somente o segundo comando por este:

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps \
  -p 5678:5678 \
  -e PYTHONPATH=/app:/app/src \
  -e DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation \
  -e PGVECTOR_COLLECTION=rastro_document_chunks \
  -v "$PWD/rastro-ai/evals:/app/evals:ro" \
  ai-indexer \
  python -Xfrozen_modules=off -m debugpy \
  --listen 0.0.0.0:5678 \
  --wait-for-client \
  -m evals.retrieval.evaluate \
  --dataset /app/evals/dataset/golden.json \
  --ks 1,3,5
```

O fluxo para usar esse comando é:

1. Deixe `evaluation-vector-db` ativo e use o comando de preparação para indexar os documentos do golden.
2. Execute o comando de debug a partir da raiz do projeto.
3. Confirme que o terminal permanece aguardando; `--wait-for-client` pausa o processo até o VS Code conectar.
4. No VS Code, execute a configuração `Docker: Python AI service`.
5. Depois da conexão, o breakpoint em `main()`, `run_evaluation()` ou nas métricas será acionado.

Se o `ai-indexer` normal já estiver ativo, ele já ocupa a porta `5678` publicada pelo Compose. Nesse caso, o comando acima falha com `Bind for 0.0.0.0:5678 failed: port is already allocated`. Existem duas formas válidas de resolver:

- parar somente o `ai-indexer` normal e manter `-p 5678:5678`:

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.langfuse.yml stop ai-indexer
  ```

- manter o `ai-indexer` normal ativo e trocar apenas a porta do host para `5679`:

  ```bash
  docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps \
    -p 5679:5678 \
    -e PYTHONPATH=/app:/app/src \
    -e DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation \
    -e PGVECTOR_COLLECTION=rastro_document_chunks \
    -v "$PWD/rastro-ai/evals:/app/evals:ro" \
    ai-indexer \
    python -Xfrozen_modules=off -m debugpy \
    --listen 0.0.0.0:5678 \
    --wait-for-client \
    -m evals.retrieval.evaluate \
    --dataset /app/evals/dataset/golden.json \
    --ks 1,3,5
  ```

  A configuração `Docker: Python AI service` já está configurada para conectar na porta `5679`. A porta `5678` continua sendo usada dentro do container; `5679` é apenas a porta publicada no host.

A configuração de attach precisa mapear também os arquivos do evaluator:

```json
{
  "localRoot": "${workspaceFolder}/rastro-ai/evals",
  "remoteRoot": "/app/evals"
}
```

O mapeamento existente de `${workspaceFolder}/rastro-ai/src` para `/app/src` deve ser preservado para os breakpoints do retriever real. Se o comando terminar imediatamente imprimindo JSON, ele foi executado sem `debugpy` ou o VS Code ainda não fez attach. O `-p HOST:5678` é necessário porque `docker compose run` não publica automaticamente as portas do serviço; `HOST` pode ser `5678` ou outra porta livre, como `5679`.

## O que acontece quando executo o comando real

```text
docker compose
├── -f docker-compose.yml
│   └── carrega a configuração principal
├── -f docker-compose.langfuse.yml
│   └── mescla a configuração complementar
└── run
    └── cria um container temporário baseado em `ai-indexer`
        ├── --rm
        │   └── remove o container ao terminar
        ├── --no-deps
        │   └── não inicia dependências automaticamente
        ├── -e PYTHONPATH=/app:/app/src
        │   ├── /app permite importar `evals`
        │   └── /app/src permite importar `rastro_ai`
        ├── -v .../evals:/app/evals:ro
        │   └── monta o evaluator e o golden em modo somente leitura
        ├── ai-indexer
        │   └── fornece banco, backend e chave de embedding pelo Compose
        ├── python -m evals.retrieval.prepare
        │   ├── carrega `dataset/golden.json`
        │   ├── usa o chunker real da aplicação
        │   ├── preserva `project_id`, `document_id` e `chunk_index`
        │   └── grava no banco `rastro_evaluation` usando a coleção `rastro_document_chunks`
        └── python -m evals.retrieval.evaluate
            ├── carrega `dataset/golden.json`
            ├── lê `--ks 1,3,5`
            ├── executa `search_relevant_chunks()`
            │   ├── gera o embedding da pergunta
            │   ├── consulta PostgreSQL/PGVector
            │   ├── filtra pelo projeto
            │   └── retorna chunks e scores
            ├── compara chunks retornados com `relevant_chunks`
            ├── calcula Recall, Precision, MRR e nDCG
            ├── verifica isolamento, scores e abstinência
            └── imprime o JSON da avaliação
```

O fluxo resumido é:

```text
golden.json
→ documents
→ chunker real
→ coleção PGVector de evaluation
→ pergunta
→ embedding real
→ PGVector
→ chunks reais
→ métricas
→ JSON
```

Este comando não chama a API NestJS, não indexa documentos durante a etapa de consulta, não gera resposta final de LLM e não usa DeepEval. Como usa `--no-deps`, `evaluation-vector-db` precisa estar ativo antes e o comando de preparação precisa ter sido executado. A variante de debug apenas envolve o mesmo módulo com `debugpy`; o fluxo de avaliação permanece igual.

## Árvore com os métodos e classes chamados

```text
evals.retrieval.evaluate.main()
├── load_dataset()
├── import rastro_ai.retrieval.search_relevant_chunks
└── run_evaluation(dataset, search_relevant_chunks, ks)
    ├── para cada caso do golden:
    │   ├── search_relevant_chunks(project_id, query, limit=5)
    │   │   └── build_semantic_search_container()
    │   │       ├── OpenAIEmbeddingRepository.from_environment()
    │   │       ├── PostgresChunkVectorStore.from_environment()
    │   │       │   └── PGVector(..., distance_strategy=COSINE)
    │   │       └── SearchRelevantChunksUseCase(vector_store)
    │   │           └── execute(project_id, query, limit=5)
    │   │               └── PostgresChunkVectorStore.search(...)
    │   │                   ├── OpenAIEmbeddingRepository.embed((query,))
    │   │                   └── PGVector.similarity_search_with_score_by_vector(...)
    │   ├── _chunk_id(result)
    │   ├── project_isolation(...)
    │   ├── score_ordering(...)
    │   ├── abstention(...)
    │   ├── recall_at_k(...)
    │   ├── precision_at_k(...)
    │   ├── reciprocal_rank(...)
    │   └── ndcg_at_k(...)
    ├── mean_reciprocal_rank(...)
    └── build_report(EvaluationResult, dataset, ks)
```

## O que cada método ou classe faz

### Entrada e preparação

- `main()`: recebe os argumentos do comando e inicia a avaliação.
- `load_dataset()`: abre o golden único e valida perguntas, projetos e chunks esperados.
- `run_evaluation()`: coordena o fluxo; não busca no banco diretamente e não gera respostas.

### Busca real

- `search_relevant_chunks()`: fachada pública usada pelo evaluator para consultar chunks.
- `build_semantic_search_container()`: monta as dependências reais do retrieval.
- `OpenAIEmbeddingRepository.from_environment()`: cria o provider de embeddings usando o ambiente.
- `PostgresChunkVectorStore.from_environment()`: cria o adapter do PGVector com distância cosine.
- `SearchRelevantChunksUseCase.execute()`: valida projeto, pergunta e limite antes de consultar o store.
- `PostgresChunkVectorStore.search()`: gera o embedding da pergunta, aplica o filtro do projeto e pede os chunks similares ao PGVector.
- `OpenAIEmbeddingRepository.embed()`: transforma a pergunta em vetor usando o modelo configurado.
- `PGVector.similarity_search_with_score_by_vector()`: executa a busca vetorial no PostgreSQL e devolve documentos com distância.

### Preparação dos resultados

- `_chunk_id()`: transforma `document_id` e índice em um ID comparável ao golden, como `meeting-db:0`.
- `project_isolation()`: verifica se todos os chunks retornados pertencem ao projeto consultado.
- `score_ordering()`: verifica se os scores retornados estão em ordem decrescente e são finitos.

### Métricas

- `abstention()`: verifica se uma consulta sem chunks relevantes retornou vazio.
- `recall_at_k()`: mede quantos chunks esperados apareceram no top-k.
- `precision_at_k()`: mede quanto do top-k retornado é relevante.
- `reciprocal_rank()`: mede a posição do primeiro chunk relevante.
- `ndcg_at_k()`: mede se os chunks mais relevantes ficaram nas melhores posições.
- `mean_reciprocal_rank()`: calcula a média do reciprocal rank entre as consultas respondíveis.

### Saída

- `build_report()`: organiza execução, resumo, scores, falhas e casos em um contrato independente de plataforma.

## Sequência exata de chamadas

Esta é a ordem de execução do fluxo real, sem agrupar etapas fora da sequência:

```text
1. evals.retrieval.evaluate.main()
   ├── 2. load_dataset()
   ├── 3. import search_relevant_chunks
   └── 4. run_evaluation(dataset, search_relevant_chunks, ks)
       └── para cada caso:
           ├── 5. cria `expected` e `relevant_ids` a partir do golden
           ├── 6. search_relevant_chunks(project_id, query, limit=5)
           │   └── 7. build_semantic_search_container()
           │       ├── 8. OpenAIEmbeddingRepository.from_environment()
           │       ├── 9. PostgresChunkVectorStore.from_environment(repository)
           │       │   ├── 10. LangChainEmbeddingAdapter(repository)
           │       │   └── 11. PGVector(..., distance_strategy=COSINE)
           │       └── 12. SearchRelevantChunksUseCase(vector_store)
           │           └── 13. execute(project_id, query, limit=5)
           │               └── 14. PostgresChunkVectorStore.search(...)
           │                   ├── 15. OpenAIEmbeddingRepository.embed((query,))
           │                   └── 16. PGVector.similarity_search_with_score_by_vector(...)
           ├── 17. `_chunk_id(result)` para cada resultado
           ├── 18. `project_isolation(...)`
           ├── 19. `score_ordering(...)`
           ├── 20. `reciprocal_rank(...)` ou `abstention(...)`
           └── para cada k em 1, 3 e 5:
               ├── 21. `recall_at_k(...)`
               ├── 22. `precision_at_k(...)`
               └── 23. `ndcg_at_k(...)`
       ├── 24. `mean_reciprocal_rank(...)`
       ├── 25. cria `EvaluationResult(...)`
       └── 26. `build_report(result, dataset, ks)`
```

### O que cada chamada faz, na mesma ordem

1. `main()` inicia o comando e lê `--dataset` e `--ks`.
2. `load_dataset()` abre e valida o golden dataset.
3. `search_relevant_chunks` é a função pública que será injetada no evaluator.
4. `run_evaluation()` controla todos os casos e agrega as métricas.
5. `expected` e `relevant_ids` representam o gabarito de chunks relevantes daquele caso.
6. `search_relevant_chunks()` inicia uma consulta real para a pergunta.
7. `build_semantic_search_container()` monta as dependências do retrieval.
8. `OpenAIEmbeddingRepository.from_environment()` lê modelo, chave e dimensão do ambiente.
9. `PostgresChunkVectorStore.from_environment()` monta o store persistente.
10. `LangChainEmbeddingAdapter` adapta o contrato de embeddings da aplicação ao LangChain.
11. `PGVector` conecta a coleção vetorial usando distância cosine.
12. `SearchRelevantChunksUseCase` recebe o store e aplica a política de consulta.
13. `execute()` valida projeto, pergunta e limite.
14. `PostgresChunkVectorStore.search()` coordena embedding da pergunta e busca vetorial.
15. `embed()` transforma a pergunta em um vetor usando OpenAI.
16. `similarity_search_with_score_by_vector()` busca os chunks mais próximos e seus scores no PGVector.
17. `_chunk_id()` converte cada resultado para `document_id:index`.
18. `project_isolation()` verifica vazamento entre projetos.
19. `score_ordering()` verifica se os scores estão em ordem decrescente.
20. `reciprocal_rank()` mede a posição do primeiro chunk relevante; `abstention()` é usado quando não há chunks esperados.
21. `recall_at_k()` mede quantos chunks esperados apareceram no top-k.
22. `precision_at_k()` mede quanto do top-k retornado é relevante.
23. `ndcg_at_k()` mede se os chunks mais relevantes ficaram nas melhores posições.
24. `mean_reciprocal_rank()` calcula a média do MRR entre os casos respondíveis.
25. `EvaluationResult` reúne métricas agregadas e diagnósticos por caso.
26. `build_report()` converte o resultado em relatório com resumo, scores, falhas e casos detalhados.
