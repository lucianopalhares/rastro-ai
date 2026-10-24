# Sequência de implementações

Este arquivo registra a ordem das tarefas de cada iniciativa. A tarefa ativa é indicada por `CURRENT.md`; nenhuma etapa posterior pode ser ativada antes da finalização da etapa anterior.

## Exemplo de validação de citações

| Ordem | Implementação | Status | Dependência | Critério de avanço |
| --- | --- | --- | --- | --- |
| 1 | `001-exemplo-validacao-citacoes` | `proposed` | nenhuma | handoff revisado pelo responsável |

Para uma nova iniciativa, registre primeiro a sequência completa. Preserve sequências anteriores e acrescente novas iniciativas sem apagar o histórico.

## API NestJS modular DDD

| Ordem | Implementação | Status | Dependência | Critério de avanço |
| --- | --- | --- | --- | --- |
| 1 | `002-criar-api-nestjs-ddd-modular` | `applied` | nenhuma | handoff aplicado; build/testes da API ainda pendentes para `verified` |

## Continuação da Fase 1 — fluxo mínimo de documentos e IA

| Ordem | Implementação | Status | Dependência | Critério de avanço |
| --- | --- | --- | --- | --- |
| 1 | `003-consolidar-ciclo-de-vida-documentos` | `verified` | `002` considerada concluída pelo responsável | contrato de documento, projeto, estados e transições cobertos por testes |
| 2 | `004-upload-minimo-de-arquivos` | verified | `003` aplicada ou verificada | `.md` e `.txt` recebidos, armazenados e associados ao documento |
| 3 | `005-extracao-e-chunking` | planejada | `004` aplicada ou verificada | texto extraído e chunks reproduzíveis gerados |
| 4 | `006-retrieval-vetorial-minimo` | planejada | `005` aplicada ou verificada | consulta retorna chunks filtrados pelo projeto |
| 5 | `007-respostas-com-citacoes` | planejada | `006` aplicada ou verificada | pergunta responde com fonte ou ausência de evidência |
| 6 | `008-evaluation-baseline` | planejada | `007` aplicada ou verificada | dataset mínimo e baseline versionado executados |
| 7 | `009-observabilidade-e-custo` | planejada | `007` aplicada ou verificada | trace registra execução, latência, tokens e custo |
| 8 | `010-autorizacao-tools-e-mcp` | planejada | `008` e `009` aplicadas ou verificadas | acesso por projeto e tools de leitura autorizadas |
