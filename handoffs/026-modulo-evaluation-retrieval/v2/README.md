# 026/v2 — Métricas desacopladas de retrieval

- Versão: `v2`; versão-base: `026/v1` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: `v1` concentrava todos os cálculos em `evaluate.py`, embora o resultado e o runtime já estivessem separados.
- Escopo autorizado: extrair Recall@k, Precision@k, MRR, nDCG, isolamento, score e abstinência para componentes puros e testáveis.
- Invariantes: sem alteração no runtime; métricas não importam LangChain, PGVector, OpenAI, dataset ou resposta de LLM.
- Arquivos reais conferidos: `rastro-ai/evals/retrieval/evaluate.py`, novo pacote `metrics/` e `rastro-ai/tests/test_retrieval_evaluation.py`.

## O que foi feito

- Cada métrica foi movida para um módulo próprio em `evals/retrieval/metrics/`, recebendo apenas IDs, relevâncias, projetos ou scores simples.
- `evaluate.py` foi reduzido ao carregamento, chamada do retriever, composição das métricas e serialização do resultado.
- A cobertura adicionou teste de composição independente das métricas, preservando os testes de integração do evaluator.

## O que muda na aplicação

- A avaliação pode testar ou substituir uma métrica sem carregar o retriever, o dataset ou o runtime da IA.
- O contrato de saída da v1 permanece compatível; o comando de integração continua chamando a fachada real somente quando solicitado.
- DeepEval continua fora do escopo e poderá consumir os mesmos goldens em módulo posterior.
- Fora do escopo: alteração de ranking, threshold de abstinência, embeddings, PGVector e geração de respostas.

## Jornada da aplicação nesta versão

Antes, uma alteração em qualquer métrica exigia navegar pelo evaluator completo. Agora, cada cálculo tem uma entrada simples, teste próprio e pode evoluir independentemente; a próxima evolução é validar o conjunto contra PGVector real.

## Como usar e validar a aplicação nesta versão

Execute os testes unitários para validar cada métrica isoladamente. Para a integração, use o mesmo comando da v1 após indexar o corpus anotado e configurar PostgreSQL/embeddings; a integração real continua manual e não foi executada nesta rodada.

## Cobertura por comportamento

- Métricas puras: `tests/test_retrieval_evaluation.py`, sem rede; cobre cada componente desacoplado.
- Composição: os testes do evaluator confirmam agregação, ranking, isolamento e abstinência.
- Integração PGVector: permanece documentada na v1 e depende de corpus e credenciais; não executada nesta rodada.

## Instruções de validação

- `PYTHONPATH=src:. python3 -m unittest -q tests.test_retrieval_evaluation`: esperado, 4 testes do módulo aprovados.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest discover -s tests -p 'test*.py' -q`: esperado, 45 testes aprovados.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md`: esperado, seis handoffs válidos.
