# 015/v7 — Preparação para reranking, chains, prompts e LangGraph

- Versão: `v7`; versão-base: `v6`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai` e imagens Docker; arquivos conferidos: portas, casos de uso de resposta/reranking, adapters LangChain, workflow, testes e dependências.
- Reconciliação: retrieval, chunking, embeddings e PGVector já estavam operacionais; ainda não existiam contratos separados para reranking, geração ou estado de grafo.

## O que foi feito

- Adicionada a porta `ChunkReranker` e o `RerankChunksUseCase`, mantendo candidatos como `RetrievedChunk`.
- Adicionada a porta `AnswerGenerator`, prompt `build_answer_prompt` e `LangChainAnswerGenerator`, exigindo texto e índices de citações verificáveis.
- Criado `LangChainReranker`, que valida a permutação de índices retornada por um Runnable LangChain.
- Criado `AnswerGraphState` e `build_answer_graph`, com etapas opcionais de retrieval, reranking e geração; o grafo não foi conectado ao runtime atual.
- Adicionada `langgraph>=1,<2` ao projeto e aos Dockerfiles; incluídos testes sem chamadas externas.

## O que muda na aplicação

- Nenhum comportamento padrão muda: o runtime continua com resposta extrativa, sem reranker, LLM ou LangGraph ativado.
- O futuro fluxo poderá trocar a implementação de reranking, prompt, modelo e orquestração sem alterar as entidades ou casos de uso centrais.
- Citações são reconstruídas apenas a partir dos chunks recebidos; índices inválidos ou fora do contexto falham explicitamente.
- Fora do escopo: escolher provider de reranking, configurar modelo generativo, ativar LangGraph, executar OpenAI/LangSmith ou alterar evaluation baseline.

## Jornada da aplicação nesta versão

Antes, o fluxo terminava no retrieval e na resposta extrativa. Agora, suas futuras etapas têm fronteiras explícitas para reranking, prompt, geração e estado LangGraph, sem mudar a experiência atual. A próxima evolução é escolher providers e executar uma comparação de qualidade, custo e latência antes de ativar geração.

## Como usar e validar a aplicação nesta versão

O uso atual permanece igual: execute retrieval e resposta extrativa normalmente. Para experimentar a preparação, injete um Runnable fake em `LangChainReranker` ou `LangChainAnswerGenerator` e compile `build_answer_graph`; o smoke externo com modelo não está ativado nesta rodada.

## Cobertura por comportamento

- Reranking: `tests/test_langchain_pipeline.py::test_reranker_reorders_existing_chunks` cobre ordem, payload e preservação dos chunks.
- Geração/citações: `test_answer_generator_validates_and_maps_citations` cobre saída estruturada e mapeamento seguro para `Citation`.
- Prompt/grafo: `test_answer_prompt_has_question_and_context_variables` e `test_answer_graph_composes_optional_steps` cobrem placeholders e composição das etapas.
- Regressão: 35 testes, evaluation `20/20`, build Docker e import do workflow no container passaram; nenhuma chamada externa foi feita.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, `35` testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python evals/evaluate.py`: esperado, `20/20` casos aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: esperado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && docker compose build ai-indexer`: esperado, imagem construída com `langgraph`.
- `cd /home/dev/dev/ia/rastro-ai && docker compose run --rm ai-indexer python -c "from rastro_ai.document_indexing.application.workflows.answer_graph import build_answer_graph; from rastro_ai.document_indexing.infrastructure.generation.langchain_answer_generator import build_answer_prompt; print(build_answer_graph.__name__, build_answer_prompt.__name__)"`: esperado, nomes das funções impressos sem erro.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v3/README.md handoffs/015-adaptar-chunking-para-langchain/v3/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v4/README.md handoffs/015-adaptar-chunking-para-langchain/v4/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v5/README.md handoffs/015-adaptar-chunking-para-langchain/v5/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v6/README.md handoffs/015-adaptar-chunking-para-langchain/v6/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v7/README.md handoffs/015-adaptar-chunking-para-langchain/v7/TIMELINE.md`: esperado, handoffs válidos.
