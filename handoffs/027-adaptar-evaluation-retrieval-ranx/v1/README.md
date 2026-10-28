# 027/v1 — Integração das métricas com ranx

- Versão-base: `026` verificada; código real conferido em `rastro-ai/evals/retrieval`, `rastro-ai/tests/test_retrieval_evaluation.py`, `rastro-ai/pyproject.toml`, `rastro-ai/Dockerfile` e `rastro-ai/Dockerfile.dev`.
- Estado encontrado: as métricas Recall, Precision, MRR e nDCG eram implementações próprias; isolamento, score ordering e abstention eram regras do projeto.
- Escopo autorizado: adicionar `ranx`, preservar os nomes/relatório atuais e adaptar somente as métricas clássicas; não incluir MAP, Hit@k ou Ragas nesta rodada.
- Invariantes: golden e IDs `document_id:index` não mudam; testes unitários não usam infraestrutura externa; o retriever de runtime não muda.

## O que foi feito

Adicionado `ranx>=0.3,<0.4` às dependências e aos Dockerfiles; criado adapter para `Qrels`/`Run`; métricas clássicas passaram a delegar o cálculo ao `ranx`; regras específicas e contrato JSON foram preservados.

## O que muda na aplicação

O evaluator mantém a mesma interface e nomes de métricas, mas usa uma implementação de ranking compatível com `ranx`; não há mudança no retrieval, embeddings, API ou geração de respostas. MAP, Hit@k, R-Precision, Ragas e DeepEval permanecem fora do escopo.

## Jornada da aplicação nesta versão

Antes, a avaliação calculava as métricas clássicas diretamente em funções locais; agora, a consulta continua produzindo chunks e scores, mas o ranking é convertido para `Qrels`/`Run` antes do cálculo; o resultado continua sendo um relatório JSON comparável.

## Como usar e validar a aplicação nesta versão

Execute o modo controlado `./rastro-ai/evals/retrieval/run_evaluation.sh test`; o container instala a dependência e executa os testes sem banco. Para a avaliação real, use `./rastro-ai/evals/retrieval/run_evaluation.sh real` após preparar o banco isolado conforme o README do retrieval.

## Cobertura por comportamento

- Métricas clássicas: `rastro-ai/tests/test_retrieval_evaluation.py`; esperado: Recall, Precision, MRR e nDCG preservados nos casos controlados.
- Regras próprias: o mesmo teste cobre isolamento, score ordering e abstention; esperado: sem alteração.
- Integração da dependência: `docker compose ... run ... tests.test_retrieval_evaluation`; esperado: `OK` no container com `ranx` instalado.
- Evaluation PGVector real: não executada automaticamente nesta rodada; depende de credenciais, banco e corpus preparados.

## Instruções de validação

```bash
bash -n rastro-ai/evals/retrieval/run_evaluation.sh
```

Resultado esperado: nenhum erro de sintaxe.

```bash
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml build ai-indexer
```

Resultado esperado: imagem construída com a dependência `ranx`.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: testes controlados terminam com `OK`, sem PostgreSQL, OpenAI ou documentos reais; a primeira execução pode levar mais tempo pela compilação JIT do Numba.
