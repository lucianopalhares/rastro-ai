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

## Estado histórico da sequência principal

- Última implementação verificada: `014-exigir-pgvector-no-runtime`.
- Próxima capacidade ativa: `015-adaptar-chunking-para-langchain`, proposta para preparar o chunking compatível com LangChain.

## Fase 1 — Integração de upload e indexação

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 10 | `012-integrar-upload-indexacao-python` | `api`/`ia`/`root` | `verified` | `004`, `005`, `011` | upload dispara indexação Python; documento chega a `ready` ou `failed`; chunks ficam consultáveis e o fluxo é coberto por testes e smoke |
| 11 | `013-configurar-debug-python-api-vscode` | `root`/`api`/`ia` | `verified` | `012` | Docker, inspector Node, debugpy, requests API/Python e fluxo API → Python documentados e verificados |
| 12 | `014-exigir-pgvector-no-runtime` | `ia` | `verified` | `013` | runtime Python exige pgvector/embeddings, fallback lexical não é selecionado silenciosamente e testes/smoke comprovam a configuração |
| 13 | `015-adaptar-chunking-para-langchain` | `ia` | `verified` | `014` | caso de uso usa `TextChunker`, adaptador LangChain preserva chunks/offsets, PGVector persiste na coleção LangChain e schema legado foi removido |

## Fase 2 — Organização evolutiva do serviço Python

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 14 | `016-reorganizar-arquitetura-python` | `ia` | `verified` | `015` | composition root explícito, fachadas sem estado global no import e testes/evaluation preservados |
| 15 | `017-renomear-fluxo-extracao-chunking` | `ia` | `verified` | `016` | nomes distinguem extração/chunking de persistência e todos os imports internos usam o vocabulário novo |
| 16 | `018-consolidar-namespaces-python` | `ia` | `proposed` | `017` | um namespace canônico por capacidade, aliases de compatibilidade documentados e imports internos consolidados |
| 17 | `019-separar-orquestracao-python` | `ia` | `proposed` | `018` | workflows LangGraph isolados de casos de uso, estado e políticas de retry/observabilidade definidos |
| 18 | `020-reorganizar-evaluation-python` | `ia` | `proposed` | `019` | runners, datasets, métricas e baselines separados, com evaluation determinística e avaliação semântica extensível |

## Estado histórico da organização evolutiva

- Última implementação da sequência: `017-renomear-fluxo-extracao-chunking`.
- Dependência: `016-reorganizar-arquitetura-python` está `verified`.
- Critério da etapa: validar a semântica dos nomes e preservar o fluxo API → Python → PGVector antes de consolidar namespaces.

## Iniciativa de governança do fluxo

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 1 | `021-revisar-fluxo-e-comentarios-handoffs` | `root` | `verified` | `017` verificada; `018`–`020` permanecem reservadas para a Fase 2 | comentários simples com histórico `NNN-vN`, contrato mínimo de versão e consistência dos estados documentados |

## Estado encerrado da iniciativa de governança

- Implementação finalizada: `021-revisar-fluxo-e-comentarios-handoffs`.
- Dependência: a implementação `017` está verificada; as alterações locais de código não relacionadas permanecem fora desta tarefa.
- Critério da etapa: regras atualizadas, handoff da versão criado, validação estrutural executada e ausência de mudança de runtime.
- Encerramento: `021` verificada; não há próxima etapa ativa nesta iniciativa.

## Iniciativa de contrato evolutivo do fluxo

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 1 | `022-contrato-evolutivo-do-fluxo-de-handoffs` | `root` | `verified` | `021` verificada | três contratos documentados, camadas estado/decisão/evidência incorporadas às regras e fluxo proporcional `small`/`normal`/`large` aplicado |

## Estado encerrado da iniciativa de contrato evolutivo

- Implementação finalizada: `022-contrato-evolutivo-do-fluxo-de-handoffs`.
- Dependência: `021` verificada; alterações locais de runtime permanecem fora do escopo.
- Critério da etapa: documentos normativos criados, regras oficiais atualizadas e validação estrutural registrada.
- Encerramento: `022` verificada; não há próxima etapa ativa e `CURRENT.md` está `idle`.

## Fase 3 — Busca semântica consumível pela API

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 19 | `023-busca-semantica-deterministica-api` | `api`/`ia` | `verified` | `011`, `014`, `015`, `017` | endpoint API → Rastro AI retorna resultados filtrados por projeto, limite, score e citações; diagnóstico de embedding documentado |

## Estado encerrado da busca semântica

- Implementação finalizada: `023-busca-semantica-deterministica-api`.
- Dependência: capacidades vetoriais anteriores verificadas; a v1 foi aplicada nas aplicações reais.
- Critério da etapa: testes, hook estrutural e smoke API → Rastro AI → PostgreSQL concluídos; `CURRENT.md` voltou a `idle`.

## Fase 4 — Observabilidade self-hosted da indexação

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 20 | `024-langfuse-observabilidade-indexacao` | `root`/`ia` | `verified` | `023` | Langfuse self-hosted acessível na porta `38917`; indexação gera trace sanitizado; modo desligado preserva o runtime |
| 21 | `025-tokens-custos-embeddings-langfuse` | `ia`/`root` | `verified` | `024` | observations de embedding registram modelo, tokens de entrada e custo inferido ou personalizado sem enviar texto |

## Estado encerrado da observabilidade

- Implementação finalizada: `025-tokens-custos-embeddings-langfuse`.
- Dependência: `024` verificada; stack Langfuse e tracing sanitizado já estão disponíveis.
- Critério da etapa: embedding informa tokens e custo inferido pelo modelo, com fallback opcional de custo direto e testes sem rede; integração confirmada pelo usuário.
- Encerramento: `025` verificada; `CURRENT.md` voltou a `idle`.

## Fase 5 — Evaluation de retrieval

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 22 | `026-modulo-evaluation-retrieval` | `ia` | `verified` | `025` | evaluator separado calcula ranking, Recall@k, Precision@k, MRR, nDCG, isolamento, score e abstinência contra golden dataset |

## Estado histórico da evaluation de retrieval

- Implementação encerrada: `026-modulo-evaluation-retrieval`.
- Última implementação: `026-modulo-evaluation-retrieval` verificada.
- Dependência: `025` verificada; runtime PGVector existente permanece inalterado.
- Critério da etapa: testes determinísticos, banco isolado, corpus compatível, execução real e validação estrutural aprovados.

## Fase 6 — Padronização das métricas de retrieval

| Ordem | Implementação | Aplicação | Status | Dependência | Critério de conclusão |
| --- | --- | --- | --- | --- | --- |
| 23 | `027-adaptar-evaluation-retrieval-ranx` | `ia` | `verified` | `026` verificada | métricas clássicas do evaluator usam `ranx`, testes controlados passam e regras específicas permanecem preservadas |

## Estado da padronização das métricas

- Implementação encerrada: `027-adaptar-evaluation-retrieval-ranx`.
- Dependência: `026` verificada; apenas o evaluator e suas dependências estão em escopo.
- Critério: testes controlados, build do container, CLI, documentação e hook estrutural aprovados; evaluation real PGVector e publicação Langfuse permanecem como próximos trabalhos.
