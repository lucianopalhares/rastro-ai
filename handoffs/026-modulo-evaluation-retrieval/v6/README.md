# 026/v6 — Documentação dos modos de evaluation

- Versão: `v6`; versão-base: `026/v5` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: comandos e métricas existiam, mas a diferença entre retriever fake e PGVector real e o critério de sucesso não estavam centralizados.
- Escopo autorizado: criar README do módulo e apontar a documentação geral para ele, sem alterar o evaluator ou o runtime.
- Invariantes: testes automatizados continuam sem rede; fluxo real continua explícito; código `0` não será tratado como qualidade aprovada sem thresholds.
- Arquivos reais conferidos: módulo retrieval, runners, golden único e README de evaluation.

## O que foi feito

- Criado `rastro-ai/evals/retrieval/README.md` com fluxo, comandos, pré-requisitos, diferenças, critérios de execução e interpretação das métricas.
- `rastro-ai/evals/README.md` passou a apontar para a documentação detalhada do módulo.

## O que muda na aplicação

- Não há mudança de runtime ou de métricas; a mudança torna explícito o que os testes automatizados comprovam e o que somente a integração real comprova.
- A documentação registra que o CLI real ainda não aplica thresholds automáticos de qualidade.
- Fora do escopo: implementar thresholds, executar PGVector real ou adicionar DeepEval.

## Jornada da aplicação nesta versão

Antes, os comandos existiam, mas era fácil confundir “testes passaram” com “busca real está boa”. Agora, a documentação separa execução técnica, qualidade do ranking e critérios de aprovação.

## Como usar e validar a aplicação nesta versão

Leia `rastro-ai/evals/retrieval/README.md`; execute primeiro os testes automatizados e depois o CLI real com banco, embeddings e corpus configurados. A integração PGVector não foi executada nesta rodada.

## Cobertura por comportamento

- Diferença entre modos: README do módulo com fluxos lado a lado.
- Evidência unitária: os testes unitários da suíte e o baseline contratual `20/20` continuam aprovados.
- Critérios de sucesso: README do módulo registra código de saída, invariantes e comparação com thresholds.
- Integração PGVector: comando e pré-requisitos documentados; execução real permanece pendente.

## Instruções de validação

- `PYTHONPATH=src:. python3 -m unittest -q tests.test_retrieval_evaluation`: esperado, testes automatizados aprovados sem rede.
- `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate --dataset evals/dataset/golden.json --ks 1,3,5`: esperado, JSON do fluxo real quando PGVector e corpus estiverem configurados; não executado nesta rodada.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md`: esperado, quatorze handoffs válidos.
