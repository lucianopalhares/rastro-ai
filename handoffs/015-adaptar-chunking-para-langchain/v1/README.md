# 015/v1 — Plano de adaptação do chunking para LangChain

- Versão: `v1`; versão-base: `014` verificada; data: 2026-10-25 -03:00; status: `proposed`.
- Aplicação: serviço Python `rastro-ai`; ordem: domínio/contrato, adaptador Python, testes/evaluation e documentação.
- Arquivos reais a conferir: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/document_indexing/domain/services.py`, `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/document_indexing/application/ports.py`, `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/document_indexing/application/use_cases/index_document.py`, `rastro-ai/src/rastro_ai/indexing.py`, `rastro-ai/tests/test_indexing.py`, `rastro-ai/evals/evaluate.py`, `rastro-ai/pyproject.toml` e `rastro-ai/README.md`.
- Estado encontrado: `TextChunker` já existe como protocolo, mas `IndexDocumentUseCase` importa diretamente `domain.services.chunk_text`; o domínio atual usa `tiktoken`, regras Markdown e cálculo próprio de offsets.
- Decisão proposta: usar `langchain-text-splitters` em um adaptador de infraestrutura, mantendo o domínio sem dependência LangChain e convertendo documentos/resultados para `DocumentChunk`.

## O que foi feito

- Criado o handoff da tarefa para preparar a migração controlada do chunking próprio para LangChain.
- Registrados os arquivos reais, invariantes, dependências e critérios de aceitação; nenhum código de aplicação foi alterado nesta rodada.
- Definida a necessidade de comparar o baseline atual antes de trocar a estratégia de divisão.

## O que muda na aplicação

- Planejado: o caso de uso passará a depender do contrato `TextChunker`, permitindo trocar a implementação atual por um adaptador LangChain.
- O domínio continuará responsável pelos contratos e entidades; LangChain ficará restrito à infraestrutura.
- O comportamento esperado preserva conteúdo, `document_id`, `project_id`, índice, offsets, sobreposição e limites de tokens.
- Fora do escopo: mudar embeddings, alterar pgvector, trocar modelo OpenAI, modificar retrieval, adicionar processamento assíncrono ou remover o chunker atual sem comparação.
- Riscos: diferenças de tokenização, offsets Unicode, separadores Markdown e qualidade do baseline; custo/latência devem ser medidos após a implementação.

## Jornada da aplicação nesta versão

Antes, o caso de uso dependia diretamente da função de chunking do domínio. A tarefa prepara uma porta estável para que o sistema possa usar LangChain no futuro sem espalhar dependências pela aplicação. Nesta rodada, a experiência da pessoa usuária não muda porque nenhuma alteração de runtime foi aplicada.

## Como usar e validar a aplicação nesta versão

Esta rodada somente registra o plano. Na implementação, o fluxo continuará sendo o upload do documento pela API, a extração Python e a divisão antes da geração de embeddings; a diferença será a implementação do chunker. A validação deverá comparar os chunks atuais e LangChain para documentos Markdown, texto Unicode, sobreposição e offsets.

## Cobertura por comportamento

- Contrato de chunking: testes unitários deverão provar que o caso de uso depende de `TextChunker`, não da função concreta do domínio.
- Compatibilidade: testes deverão preservar `DocumentChunk`, offsets, projeto, índice, limite e sobreposição.
- Regressão: evaluation baseline deverá ser executado antes/depois; qualquer divergência deverá ser registrada.
- Integração real: smoke API → Python → pgvector será necessário após a implementação; não foi executado nesta rodada.

## Instruções de validação

- `rg -n "class TextChunker|IndexDocumentUseCase|chunk_text|langchain" rastro-ai/src rastro-ai/tests rastro-ai/evals rastro-ai/pyproject.toml`: esperado, confirmar as âncoras atuais antes da aplicação.
- `uv run --project rastro-ai --with 'langchain-text-splitters' python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; print(RecursiveCharacterTextSplitter.__name__)"`: esperado, biblioteca disponível no ambiente de implementação.
- Na próxima rodada, executar `uv run --project rastro-ai python -m unittest discover -s rastro-ai/tests -p 'test_*.py'`, o runner de evaluation, `python3 -m compileall -q rastro-ai/src`, smoke HTTP e o hook estrutural.
