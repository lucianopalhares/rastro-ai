# 012/v3 — Chunking estrutural por tokens

- Versão-base: `v2` aplicada; código real reconciliado em 2026-10-24.
- Status: `applied`; aplicação: `rastro-ai`.
- Estado encontrado: o chunking padrão usava janela fixa de caracteres; a API de embeddings e o PostgreSQL estavam fora do escopo desta rodada.
- Decisão: quebrar por parágrafos/títulos Markdown, usar orçamento aproximado de 500 tokens e overlap de 60 tokens, mantendo offsets e compatibilidade legada.

## O que foi feito

O serviço de domínio passou a escolher fronteiras estruturais antes de cortar por tokens aproximados. O caso de uso e as fachadas propagam `max_tokens`/`overlap_tokens`; chamadas que informam `chunk_size` continuam usando o comportamento legado para não quebrar consumidores existentes. Foram adicionados testes de fronteiras, offsets e validações.

## O que muda na aplicação

Documentos Markdown agora tendem a manter títulos e parágrafos no mesmo chunk, reduzindo cortes no meio de uma unidade semântica. O tamanho padrão deixa de ser 800 caracteres e passa a ser aproximadamente 500 tokens, com overlap aproximado de 60 tokens. Embeddings, provider externo, API e banco não foram alterados nesta versão.

## Jornada da aplicação nesta versão

Antes, o indexador cortava o texto por uma janela fixa de caracteres. Agora, ao receber o mesmo documento, ele prioriza os limites de parágrafo/seção e usa tokens aproximados somente quando precisa dividir um bloco grande; a pessoa usuária continua recebendo o documento pesquisável, com contexto mais preservado.

## Como usar e validar a aplicação nesta versão

Execute `cd rastro-ai && python3 -m unittest discover -s tests -v`; espere os testes de chunking estrutural aprovados. Para testar manualmente, chame `chunk_text(text, document_id="doc-1", max_tokens=500, overlap_tokens=60)` e confirme que cada `content` é exatamente o slice entre `start_offset` e `end_offset` do texto normalizado.

## Cobertura por comportamento

- Chunking estrutural: evidência unitária em `tests/test_indexing.py` confirma títulos/parágrafos, offsets e reprodutibilidade.
- Configuração: evidência unitária confirma rejeição de orçamento e overlap inválidos.
- Integração/smoke: upload real curto e longo foram executados após o chunking; a API retornou `ready`, o documento longo gerou 2 chunks e ambos os embeddings foram gravados com dimensão `384`.

## Instruções de validação

- `cd rastro-ai && python3 -m unittest discover -s tests -v`: esperado, 25 testes aprovados.
- `cd rastro-ai && python3 -m compileall -q src tests`: esperado, compilação sem erros.
- `curl -fsS -X POST http://127.0.0.1:3039/api/v1/documents/upload -F projectId=project-openai-smoke -F file=@rastro-api/test/fixtures/upload/meeting.md`: esperado, `status: "ready"`; consulta SQL deve mostrar 1 chunk, conteúdo não vazio e embedding `384`.
- Upload multipart longo com `projectId=project-openai-long`: esperado, `status: "ready"`, 2 chunks, offsets válidos, conteúdo não vazio, embeddings presentes e dimensão `384` em `document_chunks`.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v2/README.md handoffs/012-integrar-upload-indexacao-python/v2/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v3/README.md handoffs/012-integrar-upload-indexacao-python/v3/TIMELINE.md`: esperado, 8 arquivos válidos.
