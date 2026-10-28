# Evaluation do Rastro AI

`dataset/golden.json` é o único golden dataset do projeto. Ele contém 20 casos anonimizados e pequenos, cobrindo retrieval, respostas fundamentadas, múltiplas fontes, ausência, conflito, citações, isolamento e prompt injection em documentos.

O mesmo arquivo é consumido pelos dois runners no container `ai-indexer`: `python -m evals.evaluate` executa o baseline extrativo, e `python -m evals.retrieval.evaluate` executa as métricas de ranking contra o retriever configurado. Comandos locais são apenas alternativa de desenvolvimento.

Cada caso possui `query`, `documents`, `relevant_chunks` e `expected_answer`. O evaluator de retrieval usa os chunks; o evaluator de resposta usa as fontes e a abstinência; `expected_answer.text` e `must_contain` ficam disponíveis para uma futura avaliação semântica.

A avaliação integrada prepara os `documents` do mesmo golden em um container PostgreSQL/PGVector separado, usando o mesmo schema e pipeline de chunking da aplicação, antes de consultar o retriever real. A diferença entre os testes automatizados com retriever fake e esse comando contra PGVector está documentada em [`retrieval/README.md`](./retrieval/README.md), incluindo comandos, pré-requisitos e critérios para interpretar uma execução bem-sucedida.

Este baseline não mede faithfulness ou relevância semântica por LLM: a aplicação atual é lexical, extrativa e não possui DeepEval, modelo, prompt ou trace de custo.

Na evaluation específica de retrieval, `ranx` fornece as métricas clássicas de ranking; regras de segurança e política de abstention permanecem no código do projeto. A avaliação contextual com Ragas ou DeepEval continua fora desta etapa.
