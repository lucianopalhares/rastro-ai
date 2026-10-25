# 015/v5 — Adaptador LangChain para embeddings

- Versão: `v5`; versão-base: `v4`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai`; arquivos reais conferidos: repository OpenAI, teste do repository, `pyproject.toml`, `Dockerfile` e `Dockerfile.dev`.
- Reconciliação: embeddings eram enviados por HTTP manual; a porta `EmbeddingRepository` e o `PostgresVectorStore` já estavam estáveis e foram preservados.

## O que foi feito

- Alterado `rastro-ai/src/rastro_ai/document_indexing/infrastructure/embeddings/openai_embedding_repository.py` para usar `langchain_openai.OpenAIEmbeddings` por trás de `OpenAIEmbeddingRepository`.
- Mantidos o batching via `embed_documents`, a ordem dos resultados, a validação de quantidade e a dimensão configurada de `384`.
- Adicionada `langchain-openai>=1,<2` ao `pyproject.toml` e aos dois Dockerfiles; o teste passou a injetar um fake compatível com a interface LangChain.

## O que muda na aplicação

- A integração de embeddings passa a usar uma biblioteca padrão do ecossistema LangChain, facilitando futura troca para outros provedores sem alterar os casos de uso.
- A Rastro continua controlando a porta `EmbeddingRepository`, a dimensão dos vetores e a persistência própria no pgvector.
- Retries e transporte passam a ser responsabilidade do adaptador LangChain; custo, latência, modelo e credencial continuam dependentes da configuração do provider.
- Fora do escopo: substituir `PostgresVectorStore`, alterar schema, mudar modelo padrão, executar chamada externa ou adicionar LangSmith.

## Jornada da aplicação nesta versão

Antes, o repository montava manualmente o payload HTTP da OpenAI. Agora, a mesma indexação usa `OpenAIEmbeddings` através do adapter local, mantendo o fluxo de chunks → embeddings → pgvector. A próxima evolução é medir a chamada real e observar custo/latência antes de trocar outras camadas.

## Como usar e validar a aplicação nesta versão

Configure `OPENAI_API_KEY`, `EMBEDDING_MODEL` e `EMBEDDING_DIMENSIONS` no ambiente do serviço e execute o fluxo normal de indexação; o caso de uso continua chamando `EmbeddingRepository`. Sem credencial, valide os testes e o import do container; o smoke real com OpenAI está indisponível nesta rodada.

## Cobertura por comportamento

- Contrato e batching: `tests/test_openai_embedding_repository.py` injeta um fake LangChain e confirma ordem, quantidade e conversão para tuplas.
- Compatibilidade: a suíte completa mantém 31 testes e `evals/evaluate.py` mantém `20/20`; o `PostgresVectorStore` não foi alterado.
- Runtime: build Docker e import de `OpenAIEmbeddings` no container passaram; integração real com OpenAI/pgvector não foi executada sem credencial.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, `31` testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python evals/evaluate.py`: esperado, `20/20` casos aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: esperado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && docker compose build ai-indexer`: esperado, imagem construída com `langchain-openai`.
- `cd /home/dev/dev/ia/rastro-ai && docker compose run --rm ai-indexer python -c "from langchain_openai import OpenAIEmbeddings; import rastro_ai; print(OpenAIEmbeddings.__name__)"`: esperado, `OpenAIEmbeddings` impresso sem erro.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v3/README.md handoffs/015-adaptar-chunking-para-langchain/v3/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v4/README.md handoffs/015-adaptar-chunking-para-langchain/v4/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v5/README.md handoffs/015-adaptar-chunking-para-langchain/v5/TIMELINE.md`: esperado, handoffs válidos.
