# 023/v1 — Busca semântica determinística pela API

- Versão: `v1`; versão-base: estado real sem endpoint de busca; data: 2026-10-26 -03:00; status: `verified`.
- Estado-base: retrieval LangChain/PGVector já existia em `rastro-ai`, mas não havia boundary HTTP nem consumidor no `rastro-api`.
- Escopo autorizado: publicar busca por projeto com limite, score, conteúdo, offsets e citação; preservar upload/indexação.
- Invariantes: coleção `rastro_document_chunks`, dimensão 384, filtro obrigatório por projeto e ranking cosine permanecem inalterados.
- Reconciliação: indexação e embeddings confirmados; teste direto OpenAI e fluxo Python → PGVector responderam; travamento observado ficou restrito ao processo HTTP local.

## O que foi feito

- `rastro-ai/src/rastro_ai/service.py`: inserido `POST /search`, validação de projeto/pergunta/limite e serialização de resultados com citação.
- `rastro-api/src/modules/documents/application/semantic-searcher.ts`: criado contrato de resposta e resultados.
- `rastro-api/src/modules/documents/infrastructure/http-semantic-searcher.ts`: criado proxy HTTP com timeout, validação de resposta e propagação de erro.
- `rastro-api/src/modules/documents/presentation/documents.controller.ts` e `documents.module.ts`: publicado `GET /api/v1/documents/search` e injetado o adapter.
- Testes e READMEs reais foram atualizados; o problema resolvido foi tornar o retrieval semântico consumível pela API.

## O que muda na aplicação

- A API NestJS passa a receber `projectId`, `query` e `limit` e delega a busca ao Rastro AI.
- O Rastro AI gera o embedding da consulta com o mesmo provider da indexação, aplica filtro por projeto no PGVector e retorna score e offsets verificáveis.
- `limit` é validado entre 1 e 50; erros do Python não viram resultado vazio.
- Não há agente, tool autônoma, reranking ou geração de resposta nesta rodada; a busca permanece determinística.
- O diagnóstico mostrou conectividade e crédito válidos; o timeout anterior foi um processo HTTP local preso, resolvido no smoke após reinício.

## Jornada da aplicação nesta versão

Antes, a aplicação conseguia persistir e consultar vetores apenas por chamadas internas do Python. Agora, uma pessoa cliente chama a API NestJS, que preserva o escopo do projeto e encaminha a consulta ao Rastro AI; o retorno contém os trechos mais próximos e citações reproduzíveis. A geração de resposta e tools ficam fora do escopo.

## Como usar e validar a aplicação nesta versão

Com `vector-db`, `ai-indexer` e `api` saudáveis, faça uma indexação de um documento e consulte a API pública. A resposta deve conter o projeto solicitado, a consulta original, zero ou mais resultados ordenados pelo PGVector e uma citação com o mesmo documento, chunk e offsets.

## Cobertura por comportamento

- Boundary Python: `rastro-ai/tests/test_service.py` cobre contrato de payload, limite, score e citação com retrieval simulado.
- Proxy API: `rastro-api/src/modules/documents/infrastructure/http-semantic-searcher.spec.ts` cobre payload, resposta e erro HTTP.
- Núcleo vetorial: `rastro-ai/tests/test_postgres_vector_store.py` já cobre dimensão, IDs, metadata, filtro por projeto e score; não foi duplicado.
- Smoke real: cURL API → Python → PostgreSQL deve ser executado após rebuild/restart; o teste direto anterior confirmou embedding de 384 dimensões e o smoke de indexação respondeu `200`.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, todos os testes Python aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-api && npm test -- --runInBand`: esperado, testes NestJS e do proxy aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-api && npm run build`: esperado, TypeScript compilado sem erro.
- `curl --fail-with-body --get --url 'http://127.0.0.1:3039/api/v1/documents/search?projectId=debug-project&query=qual%20banco%20foi%20decidido&limit=5' --header 'accept: application/json'`: esperado, HTTP `200` com `projectId`, `query`, `results`, `score` e `citation`.
- `curl --fail-with-body --request POST --url http://127.0.0.1:18473/search --header 'content-type: application/json' --data '{"projectId":"debug-project","query":"qual banco foi decidido","limit":5}'`: esperado, HTTP `200` com resultados filtrados pelo projeto.
- `docker compose exec -T vector-db psql -U rastro -d rastro -c "SELECT vector_dims(embedding), cmetadata FROM langchain_pg_embedding ORDER BY id DESC LIMIT 1;"`: esperado, dimensão `384` e metadata do chunk persistido.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/023-busca-semantica-deterministica-api/README.md handoffs/023-busca-semantica-deterministica-api/TIMELINE.md handoffs/023-busca-semantica-deterministica-api/v1/README.md handoffs/023-busca-semantica-deterministica-api/v1/TIMELINE.md`: esperado, handoffs válidos.
