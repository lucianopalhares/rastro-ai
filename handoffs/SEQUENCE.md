# Sequência de capacidades do Rastro AI

Esta sequência organiza as capacidades entregues nas aplicações reais e na raiz do projeto, com suas dependências e critérios de conclusão.

## Iniciativas anteriores

| Ordem | Implementação | Aplicação | Status | Critério |
| --- | --- | --- | --- | --- |
| 1 | `001-exemplo-validacao-citacoes` | raiz | `proposed` | citações validadas no fluxo de documentação |
| 2 | `002-criar-api-nestjs-ddd-modular` | `api` | `applied` | API modular criada; build/testes pendentes para `verified` |

## Fase 1 — fluxo mínimo de documentos e IA

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 1 | `003-consolidar-ciclo-de-vida-documentos` | `api` | `verified` | `002` | contrato, projeto, estados e transições cobertos por testes |
| 2 | `004-upload-minimo-de-arquivos` | `api` | `verified` | `003` | `.md` e `.txt` recebidos, armazenados e associados; smoke HTTP `201` com estado `pending` |
| 3 | `005-extracao-e-chunking` | `ia` | `verified` | `004` | texto extraído e chunks reproduzíveis gerados |
| 4 | `006-retrieval-vetorial-minimo` | `ia` | `verified` | `005` | consulta retorna chunks filtrados pelo projeto |
| 5 | `007-respostas-com-citacoes` | `ia` | `verified` | `006` | pergunta responde com fonte ou ausência de evidência |
| 6 | `008-evaluation-baseline` | `ia` | `verified` | `007` | dataset mínimo e baseline versionado executados |
| 7 | `011-persistencia-vetorial-pgvector` | `root`/`ia` | `verified` | `008` | PostgreSQL com pgvector, volume e busca semântica persistente |
| 8 | `009-observabilidade-e-custo` | `ia` | `proposed` | `007` e `011` | trace registra execução, latência, tokens e custo; standby |
| 9 | `010-autorizacao-tools-e-mcp` | `api`/`ia` | `proposed` | `008`, `009` e `011` | acesso por projeto e tools de leitura autorizadas; standby |

## Estado ativo

- Última implementação verificada: `014-exigir-pgvector-no-runtime`.
- Próxima capacidade ativa: `015-adaptar-chunking-para-langchain`, proposta para preparar o chunking compatível com LangChain.

## Fase 1 — Integração de upload e indexação

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 10 | `012-integrar-upload-indexacao-python` | `api`/`ia`/`root` | `verified` | `004`, `005`, `011` | upload dispara indexação Python; documento chega a `ready` ou `failed`; chunks ficam consultáveis e o fluxo é coberto por testes e smoke |
| 11 | `013-configurar-debug-python-api-vscode` | `root`/`api`/`ia` | `verified` | `012` | Docker, inspector Node, debugpy, requests API/Python e fluxo API → Python documentados e verificados |
| 12 | `014-exigir-pgvector-no-runtime` | `ia` | `verified` | `013` | runtime Python exige pgvector/embeddings, fallback lexical não é selecionado silenciosamente e testes/smoke comprovam a configuração |
| 13 | `015-adaptar-chunking-para-langchain` | `ia` | `verified` | `014` | caso de uso usa `TextChunker`, adaptador LangChain preserva chunks/offsets, PGVector persiste na coleção LangChain e schema legado foi removido |
