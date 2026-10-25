# 012/v4 — Tokenizer real no chunking

- Versão-base: `v3` aplicada; código real reconciliado em 2026-10-24.
- Status: `applied`; aplicação: `rastro-ai`.
- Estado encontrado: o chunking já respeitava estrutura, mas estimava tokens com regex de palavras.
- Decisão: usar `tiktoken.encoding_for_model("text-embedding-3-small")`, mantendo cortes estruturais, offsets UTF-8 e parâmetros legados.

## O que foi feito

Foi adicionada a dependência `tiktoken` e o domínio passou a derivar intervalos de caracteres a partir dos tokens reais do modelo de embedding. O Dockerfile instala a biblioteca junto das dependências Python e os testes cobrem Unicode, offsets e múltiplos chunks.

## O que muda na aplicação

O orçamento padrão de 500 tokens e o overlap de 60 tokens agora são calculados pelo tokenizer do modelo, não por aproximação de palavras. Títulos/parágrafos continuam sendo priorizados. API, embeddings, banco e chamadas externas não mudam nesta versão.

## Jornada da aplicação nesta versão

Antes, o chunking chamava a política estrutural usando uma estimativa por palavras. Agora, o mesmo upload usa os tokens reais do `text-embedding-3-small`, reduzindo o risco de exceder o orçamento do embedding sem perder offsets ou fronteiras de seção.

## Como usar e validar a aplicação nesta versão

Execute `cd rastro-ai && python3 -m unittest discover -s tests -v`; espere os testes de tokenizer e chunking aprovados. O fluxo API → embeddings → PostgreSQL permanece validado pelas versões anteriores e não precisa ser repetido para esta alteração isolada.

## Cobertura por comportamento

- Tokenização real: evidência unitária em `tests/test_indexing.py` cobre texto Unicode, múltiplos chunks e slices por offset.
- Compatibilidade estrutural: evidência unitária mantém títulos/parágrafos e os parâmetros legados.
- Integração/smoke: não repetida nesta versão porque API, provider de embeddings e schema não foram alterados.

## Instruções de validação

- `cd rastro-ai && python3 -m unittest discover -s tests -v`: esperado, 26 testes aprovados.
- `cd rastro-ai && python3 -m compileall -q src tests`: esperado, compilação sem erros.
- `docker compose build ai-indexer`: esperado, imagem Python construída com `tiktoken`.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v2/README.md handoffs/012-integrar-upload-indexacao-python/v2/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v3/README.md handoffs/012-integrar-upload-indexacao-python/v3/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v4/README.md handoffs/012-integrar-upload-indexacao-python/v4/TIMELINE.md`: esperado, 10 arquivos válidos.
