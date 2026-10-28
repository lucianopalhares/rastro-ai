# 026/v15 — Corpus e banco isolado de evaluation

- Versão: `v15`; versão-base: `026/v14` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: o golden já continha `expected_answer`, mas o evaluation real consultava o banco de desenvolvimento, cujo corpus não correspondia a `documents`, `project_id` e `relevant_chunks` do golden.
- Escopo autorizado: preparar corpus pelo pipeline real, adicionar container PostgreSQL/PGVector isolado, preservar resposta no golden e documentar os comandos; sem alterar o banco original.
- Invariantes: o golden continua único; `expected_answer` permanece no mesmo arquivo; testes unitários não usam rede; o banco de evaluation usa a mesma imagem e schema do banco principal.
- Arquivos reais alterados: `docker-compose.yml`, `rastro-ai/evals/retrieval/prepare.py`, `rastro-ai/evals/retrieval/evaluate.py`, `rastro-ai/evals/retrieval/README.md`, `rastro-ai/evals/README.md` e `rastro-ai/tests/test_retrieval_evaluation.py`.

## O que foi feito

- Criado `evals.retrieval.prepare`, que lê `documents` e `expected_answer` do golden, usa o chunker real e faz upsert dos chunks.
- Adicionado `evaluation-vector-db`, baseado em `pgvector/pgvector:pg16`, com banco `rastro_evaluation`, volume próprio e o mesmo init do banco original.
- Atualizados os comandos para usar `DATABASE_URL` do banco isolado e mantido `expected_answer` no golden para os evaluators de resposta.
- Adicionado teste do contrato corpus/golden sem rede.

## O que muda na aplicação

- A evaluation integrada deixa de depender dos documentos de debug do `vector-db` principal.
- A preparação é idempotente por IDs determinísticos e usa o mesmo chunker da aplicação; a consulta continua passando pelo retriever real.
- Não há alteração no runtime do `ai-indexer`, na API, no banco principal ou no cálculo das métricas.

## Jornada da aplicação nesta versão

O Compose inicia `evaluation-vector-db`; `evals.retrieval.prepare` lê o golden e indexa seu corpus; `evals.retrieval.evaluate` consulta o mesmo banco isolado e compara os chunks retornados com `relevant_chunks`, enquanto `expected_answer` fica disponível para a futura avaliação de resposta.

## Como usar e validar a aplicação nesta versão

Use os comandos completos da seção de validação do README do retrieval: subir `evaluation-vector-db`, preparar o corpus e executar o evaluator com a mesma `DATABASE_URL`.

## Cobertura por comportamento

- Compatibilidade: documentos, projetos, IDs, chunks e respostas vêm do mesmo golden.
- Isolamento: o banco de evaluation possui serviço, volume e database próprios.
- Pipeline real: chunking, embedding, persistência PGVector e retrieval permanecem reais.
- Resposta esperada: `expected_answer` continua no golden e não é misturada às métricas de retrieval.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml config --quiet`: esperado, configuração válida com `evaluation-vector-db`.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d evaluation-vector-db`: esperado, container saudável na rede Compose sem publicar porta no host.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, 5 testes e `OK`.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Preparação integrada: executar os comandos do README quando `OPENAI_API_KEY` estiver configurada; esperado, JSON com `case_count` e `chunk_count` sem traceback.
- Evaluation integrada: executar o evaluator usando `DATABASE_URL=postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation`; esperado, chunks compatíveis com o golden e métricas não zeradas nos casos respondíveis.
- Validação integrada/manual: não aplicada nesta rodada porque `OPENAI_API_KEY` não está configurada; essa etapa chama o provider de embeddings e pode gerar custo externo.
- Estado desta rodada: a preparação/evaluation integrada não foi executada porque `OPENAI_API_KEY` não está configurada; o container foi validado saudável e o teste sem rede passou.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
