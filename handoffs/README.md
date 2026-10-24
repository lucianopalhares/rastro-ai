# Estado das aplicações do Rastro AI

- Raiz: a iniciativa está na Fase 1; `CURRENT.md` aponta para `005-extracao-e-chunking`.
- API (`rastro-api`): a tarefa `004` está `verified`; a API recebe `.md` e `.txt` não vazios, armazena localmente, associa ao projeto/documento e retorna `status: pending`.
- Frontend (`rastro-front`): nenhuma capacidade desta sequência foi aplicada ainda.
- IA (`rastro-ai`): extração, chunking, retrieval, respostas e evaluation ainda dependem das etapas seguintes.
- Invariantes atuais: o upload não inicia extração nem indexação; o armazenamento local e o processamento assíncrono permanecem limitados ao escopo atual.
- Próxima capacidade: `005-extracao-e-chunking`, dependente do upload verificado.

## Implementações registradas

| Número | Implementação | Aplicação | Estado |
| --- | --- | --- | --- |
| `001` | `exemplo-validacao-citacoes` | raiz | `proposed` |
| `002` | `criar-api-nestjs-ddd-modular` | `api` | `applied` |
| `003` | `consolidar-ciclo-de-vida-documentos` | `api` | `verified` |
| `004` | `upload-minimo-de-arquivos` | `api` | `verified` |

Este resumo representa o estado funcional conhecido das aplicações e da raiz após a conclusão da tarefa `004`.
