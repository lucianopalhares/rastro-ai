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
| 3 | `005-extracao-e-chunking` | `ia` | `proposed` | `004` | texto extraído e chunks reproduzíveis gerados |
| 4 | `006-retrieval-vetorial-minimo` | `ia` | `proposed` | `005` | consulta retorna chunks filtrados pelo projeto |
| 5 | `007-respostas-com-citacoes` | `ia` | `proposed` | `006` | pergunta responde com fonte ou ausência de evidência |
| 6 | `008-evaluation-baseline` | `ia` | `proposed` | `007` | dataset mínimo e baseline versionado executados |
| 7 | `009-observabilidade-e-custo` | `ia` | `proposed` | `007` | trace registra execução, latência, tokens e custo |
| 8 | `010-autorizacao-tools-e-mcp` | `api`/`ia` | `proposed` | `008` e `009` | acesso por projeto e tools de leitura autorizadas |

## Estado ativo

- Implementação ativa: `005-extracao-e-chunking`.
- Próxima capacidade: extração e chunking do conteúdo recebido pela API.
