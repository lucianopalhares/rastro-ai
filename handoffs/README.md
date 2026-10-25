# Estado das aplicações do Rastro AI

- Raiz: a iniciativa está na Fase 1; `CURRENT.md` mantém a última implementação finalizada `015-adaptar-chunking-para-langchain` até a abertura de uma nova tarefa.
- API (`rastro-api`): a tarefa `004` está `verified`; a API recebe `.md` e `.txt` não vazios, armazena localmente, associa ao projeto/documento e retorna `status: pending`.
- Frontend (`rastro-front`): nenhuma capacidade desta sequência foi aplicada ainda.
- IA (`rastro-ai`): extração/chunking, embeddings e PGVector com LangChain, retrieval e respostas extrativas com citações estão verificados; reranking, chains, prompts e LangGraph permanecem preparados para evolução futura.
- Invariantes atuais: o upload preserva o arquivo original, envia o conteúdo ao indexador Python e retorna `ready` ou `failed`; retry assíncrono permanece fora do escopo.
- Próxima capacidade ativa: `017-consolidar-namespaces-python`; a implementação `016-reorganizar-arquitetura-python` foi verificada e finalizada.

## Implementações registradas

| Número | Implementação | Aplicação | Estado |
| --- | --- | --- | --- |
| `001` | `exemplo-validacao-citacoes` | raiz | `proposed` |
| `002` | `criar-api-nestjs-ddd-modular` | `api` | `applied` |
| `003` | `consolidar-ciclo-de-vida-documentos` | `api` | `verified` |
| `004` | `upload-minimo-de-arquivos` | `api` | `verified` |
| `005` | `extracao-e-chunking` | `ia` | `verified` |
| `006` | `retrieval-vetorial-minimo` | `ia` | `verified` |
| `007` | `respostas-com-citacoes` | `ia` | `verified` |
| `011` | `persistencia-vetorial-pgvector` | `root`/`ia` | `verified` |
| `012` | `integrar-upload-indexacao-python` | `api`/`ia`/`root` | `verified` |
| `014` | `exigir-pgvector-no-runtime` | `ia` | `verified` |
| `015` | `adaptar-chunking-para-langchain` | `ia` | `verified` |
| `016` | `reorganizar-arquitetura-python` | `ia` | `verified` |

## Padrão de validação para novas versões

Cada novo `vN/README.md` deve incluir `## Jornada da aplicação nesta versão`, `## Como usar e validar a aplicação nesta versão` e `## Cobertura por comportamento` antes de `## Instruções de validação`. Registre o propósito, a evolução para a pessoa usuária, o request completo ou os passos de frontend quando existirem e, caso a integração ainda não exista, a limitação e a validação executável disponível; handoffs históricos permanecem válidos sem retroatividade.

Este resumo representa o estado funcional conhecido das aplicações e da raiz após a verificação da tarefa `012`; o runtime possui upload, indexação Python e persistência vetorial integrados.
