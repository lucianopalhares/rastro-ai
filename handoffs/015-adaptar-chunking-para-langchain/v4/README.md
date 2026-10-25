# 015/v4 — Unificação dos caminhos públicos de chunking

- Versão: `v4`; versão-base: `v3`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai`; arquivos reais conferidos: `src/rastro_ai/indexing.py` e `tests/test_indexing.py`.
- Reconciliação: `index_document` já usava `LangChainTextChunker`, mas `indexing.chunk_text` ainda importava o chunker de domínio diretamente.

## O que foi feito

- Alterado `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/indexing.py` para instanciar e reutilizar `LangChainTextChunker` na fachada pública `chunk_text`.
- Removido desse caminho o import local de `chunking.domain.chunker`; o serviço de domínio antigo não foi apagado nesta rodada.
- Adicionado teste em `rastro-ai/tests/test_indexing.py` para verificar offsets, projeto e uso da mesma estratégia LangChain.

## O que muda na aplicação

- Chamadas públicas a `chunk_text` e o fluxo `index_document` agora produzem chunks pela mesma estratégia.
- A API legada e os parâmetros existentes permanecem disponíveis; offsets, `project_id`, índice e validações continuam sob responsabilidade do adaptador.
- O serviço de domínio antigo permanece somente para compatibilidade interna e testes históricos; sua remoção exige confirmar consumidores restantes.
- Fora do escopo: trocar embeddings, alterar pgvector, remover a fachada, medir custo/latência ou mudar o retrieval.

## Jornada da aplicação nesta versão

Antes, uma pessoa integradora poderia obter chunks diferentes chamando diretamente `chunk_text` ou indexando um arquivo. Agora, os dois caminhos passam pelo mesmo adaptador LangChain e têm comportamento convergente. A próxima evolução é remover o código antigo somente após uma busca de consumidores e uma decisão explícita de compatibilidade.

## Como usar e validar a aplicação nesta versão

Na raiz `rastro-ai/`, use `indexing.chunk_text(text, document_id=..., project_id=...)` ou `index_document(document_id, path, project_id=...)`; ambos usam LangChain. Execute a suíte Python para confirmar offsets e metadados; o smoke API → Python → pgvector continua dependente do ambiente externo.

## Cobertura por comportamento

- Convergência pública: `tests/test_indexing.py::test_public_chunk_text_uses_langchain_strategy` cobre o caminho direto com offsets, conteúdo e projeto.
- Contrato compartilhado: `test_use_case_delegates_chunking_to_port` e `test_langchain_chunker_preserves_offsets_and_project` cobrem injeção e conversão do adaptador.
- Regressão: 31 testes e evaluation `20/20` passaram; integração HTTP/smoke completo não foi alterado nesta rodada e permanece fora do escopo.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, `31` testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python evals/evaluate.py`: esperado, `20/20` casos aprovados e métricas em `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: esperado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v3/README.md handoffs/015-adaptar-chunking-para-langchain/v3/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v4/README.md handoffs/015-adaptar-chunking-para-langchain/v4/TIMELINE.md`: esperado, handoffs válidos.
