# Estado das aplicações do Rastro AI

- Raiz: a iniciativa está na Fase 1; `CURRENT.md` aponta para `007-respostas-com-citacoes`.
- API (`rastro-api`): a tarefa `004` está `verified`; a API recebe `.md` e `.txt` não vazios, armazena localmente, associa ao projeto/documento e retorna `status: pending`.
- Frontend (`rastro-front`): nenhuma capacidade desta sequência foi aplicada ainda.
- IA (`rastro-ai`): extração/chunking e retrieval lexical determinístico em memória estão verificados; respostas e evaluation dependem das etapas seguintes.
- Invariantes atuais: o upload não inicia extração nem indexação; o armazenamento local e o processamento assíncrono permanecem limitados ao escopo atual.
- Próxima capacidade: `007-respostas-com-citacoes`, dependente do retrieval verificado.

## Implementações registradas

| Número | Implementação | Aplicação | Estado |
| --- | --- | --- | --- |
| `001` | `exemplo-validacao-citacoes` | raiz | `proposed` |
| `002` | `criar-api-nestjs-ddd-modular` | `api` | `applied` |
| `003` | `consolidar-ciclo-de-vida-documentos` | `api` | `verified` |
| `004` | `upload-minimo-de-arquivos` | `api` | `verified` |
| `005` | `extracao-e-chunking` | `ia` | `verified` |
| `006` | `retrieval-vetorial-minimo` | `ia` | `verified` |

## Padrão de validação para novas versões

Cada novo `vN/README.md` deve incluir `## Jornada da aplicação nesta versão`, `## Como usar e validar a aplicação nesta versão` e `## Cobertura por comportamento` antes de `## Instruções de validação`. Registre o propósito, a evolução para a pessoa usuária, o request completo ou os passos de frontend quando existirem e, caso a integração ainda não exista, a limitação e a validação executável disponível; handoffs históricos permanecem válidos sem retroatividade.

Este resumo representa o estado funcional conhecido das aplicações e da raiz após a conclusão da tarefa `004`.
