# 026/v17 — Atalho de evaluation na raiz

- Versão: `v17`; versão-base: `026/v16` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: o script funcionava em `rastro-ai/evals/retrieval`, mas exigia conhecer o caminho interno do módulo.
- Escopo autorizado: criar um atalho na raiz que encaminha argumentos ao script original e atualizar a documentação.
- Invariantes: existe uma única implementação real; todos os argumentos são preservados; os modos `test` e `real` continuam iguais.
- Arquivos reais alterados: `run_evaluation.sh` e `rastro-ai/evals/retrieval/README.md`.

## O que foi feito

- Criado `run_evaluation.sh` na raiz do projeto.
- O atalho resolve seu próprio diretório e usa `exec` para chamar o script original.
- A documentação passou a usar o comando curto a partir da raiz.

## O que muda na aplicação

- O usuário pode executar `./run_evaluation.sh test` ou `./run_evaluation.sh real` sem conhecer o caminho interno.
- A lógica permanece exclusivamente em `rastro-ai/evals/retrieval/run_evaluation.sh`.
- Não há mudança no runtime, nas métricas ou no banco.

## Jornada da aplicação nesta versão

O shell da raiz recebe os argumentos, encaminha-os ao script original e preserva o mesmo modo, opções, saída e código de retorno.

## Como usar e validar a aplicação nesta versão

A partir da raiz, execute `./run_evaluation.sh test`; para o fluxo real, use `./run_evaluation.sh real`.

## Cobertura por comportamento

- Atalho: o script da raiz chama o script original.
- Argumentos: `test`, `real`, `--prepare` e `--ks` são preservados.
- Implementação única: nenhum código de avaliação foi duplicado.

## Instruções de validação

- `bash -n run_evaluation.sh rastro-ai/evals/retrieval/run_evaluation.sh`: esperado, sintaxe válida.
- `./run_evaluation.sh test`: esperado, 5 testes e `OK`.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Evidência unitária: o atalho deve produzir o mesmo resultado do script original no modo `test`.
- Validação integrada/manual: não executada nesta rodada; o modo real depende do banco de evaluation e de `OPENAI_API_KEY`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
