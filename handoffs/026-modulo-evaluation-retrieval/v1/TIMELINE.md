# Timeline — 026/v1 módulo de evaluation de retrieval

## 2026-10-27 -03:00 — aplicação v1

- Status: `proposed`.
- Arquivos reais: `rastro-ai/evals/retrieval/`, `rastro-ai/tests/test_retrieval_evaluation.py` e controles da implementação 026.
- Mudanças aplicadas: evaluator injetável, golden dataset, métricas de ranking, isolamento, score e abstinência; runtime preservado.
- Evidência esperada: testes determinísticos sem rede e hook estrutural aprovados; integração PGVector fica explícita e manual.
- Pendência: executar a rodada de verificação e registrar o resultado do corpus real anotado.

## 2026-10-27 -03:00 — aplicação

- Status: `applied`.
- Evidência: 3 testes do módulo, 44 testes Python no container e hook estrutural aprovados.
- Limite: o comando PGVector não foi executado por depender de corpus/credenciais externos ao teste determinístico.
- Controle: implementação permanece ativa para a rodada de integração real.
