# 015/v2 — Aplicação do adaptador LangChain

- Versão: `v2`; versão-base: `v1`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai`; arquivos reais conferidos: `pyproject.toml`, porta, caso de uso, fachada, testes e serviço de chunking atual.
- Reconciliação: o contrato existia, mas não era injetado; `IndexDocumentUseCase` importava `chunk_text` diretamente; adaptador LangChain estava ausente.
- Decisão: `RecursiveCharacterTextSplitter` fica na infraestrutura; o modo padrão conta tokens com `tiktoken`, e o modo legado mantém limites em caracteres.

## O que foi feito

- Adicionada a dependência `langchain-text-splitters>=0.3,<1` em `/home/dev/dev/ia/rastro-ai/rastro-ai/pyproject.toml`.
- Alterado `document_indexing/application/ports.py` para formalizar `TextChunker` com projeto, limites e retorno de `DocumentChunk`.
- Alterado `document_indexing/application/use_cases/index_document.py` para receber e chamar a porta, removendo o import direto do serviço de domínio.
- Criado `document_indexing/infrastructure/chunking/langchain_text_chunker.py`, com normalização, separadores Markdown, contagem por tokens/caracteres, conversão e correção defensiva de offsets sobrepostos.
- Alterado `indexing.py` para compor `IndexDocumentUseCase` com `LangChainTextChunker`; adicionados testes de delegação, offsets, índice e `project_id`.

## O que muda na aplicação

- A indexação real passa a usar o adaptador LangChain, sem expor LangChain ao domínio ou ao caso de uso.
- `DocumentChunk`, conteúdo, offsets, índice, projeto e validações de configuração permanecem no contrato aplicado; a fachada `chunk_text` legada continua usando o serviço anterior.
- O baseline de evaluation permaneceu em `20/20`, sem alteração de embeddings, retrieval, banco, custo ou observabilidade; diferenças de segmentação devem ser acompanhadas em evolução futura.
- Fora do escopo: smoke HTTP com serviços externos, troca de embeddings, remoção do chunker legado e medição formal de latência/custo.

## Jornada da aplicação nesta versão

Antes, o fluxo de indexação extraía o arquivo e chamava diretamente o serviço de domínio. Agora, a pessoa responsável pelo sistema pode trocar a estratégia atrás de `TextChunker`, enquanto o fluxo continua produzindo chunks indexáveis com metadados. O resultado percebido permanece equivalente nos contratos cobertos; a próxima evolução é comparar qualidade e latência em documentos reais.

## Como usar e validar a aplicação nesta versão

Na raiz `rastro-ai/`, instale a dependência declarada e execute `python -m unittest discover -s tests -p 'test_*.py'`. O uso programático continua sendo `index_document(document_id, path, project_id=...)`; o endpoint integrado API → Python → pgvector não foi executado nesta rodada porque smoke externo está fora do escopo.

## Cobertura por comportamento

- Porta do caso de uso: `tests/test_indexing.py::test_use_case_delegates_chunking_to_port` prova por teste contratual que o texto e os parâmetros chegam ao `TextChunker` injetado.
- Conversão LangChain: `tests/test_indexing.py::test_langchain_chunker_preserves_offsets_and_project` cobre conteúdo, offsets Unicode, índice, projeto e sobreposição.
- Regressão: os 30 testes da suíte e `evals/evaluate.py` mantiveram o baseline em `20/20`; integração HTTP/smoke real não se aplica à rodada e permanece pendente para validação final.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, `30` testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python evals/evaluate.py`: esperado, `20/20` casos aprovados e métricas `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: esperado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md`: esperado, handoffs válidos.
