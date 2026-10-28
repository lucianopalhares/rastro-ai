# Evaluation profissional do retriever

Este documento complementa o [README da evaluation de retrieval](README.md). Ele separa o que o Rastro AI já executa do que uma operação profissional precisa controlar para transformar métricas em uma decisão confiável de qualidade.

## 1. Thresholds e gate de qualidade

### Objetivo

Uma evaluation só apoia uma decisão quando existe uma regra explícita para aprovar, reprovar ou apenas observar uma execução. Métricas sem limite não impedem regressões: uma busca pode piorar e o processo ainda terminar com sucesso.

### Como implementar profissionalmente

Manter thresholds versionados por conjunto de dados, produto e cenário. Separar limites por natureza:

- segurança: `project_isolation = 1.0` e `score_ordering = 1.0`;
- relevância: limites mínimos para `Recall@k`, `Precision@k`, `MRR` e `nDCG@k`;
- abstention: desempenho mínimo nos casos sem evidência;
- operação: limite máximo de P95, taxa de erro e taxa de resultado vazio.

O avaliador deve produzir estados distintos, por exemplo `passed`, `failed` e `not_evaluated`, informar qual threshold falhou e retornar código de saída diferente de zero em falha bloqueadora. Thresholds não devem ser escolhidos depois de observar o resultado da mesma execução.

### Como encaixar na aplicação atual

O relatório atual já possui `quality.status`, `quality.thresholds` e `quality.checks`, mas retorna `not_evaluated` com thresholds vazios em [`report.py`](report.py). O próximo passo é adicionar um arquivo versionado, como `thresholds/v1.json`, carregá-lo em `build_report()` e fazer `run_evaluation.sh` falhar quando uma regra crítica for violada. A primeira política pode proteger isolamento, ordenação e erro antes de estabelecer metas de relevância.

## 2. Governança do golden dataset

### Objetivo

O dataset precisa representar as perguntas e documentos relevantes do produto, e não apenas os exemplos que confirmam que a implementação atual funciona.

### Como implementar profissionalmente

Versionar o schema, os casos, a origem dos exemplos e a decisão de relevância. Para cada caso, registrar a intenção da consulta, o projeto, os documentos candidatos, os chunks relevantes, o grau de relevância e o comportamento esperado quando não houver evidência.

Manter conjuntos separados para desenvolvimento, validação e teste oculto quando possível. Definir cobertura mínima por categoria, casos difíceis, consultas sem resposta, conflitos, isolamento entre projetos, documentos longos e variações de linguagem. Quando houver julgamento humano, registrar critérios, revisão e, se aplicável, concordância entre avaliadores.

### Como encaixar na aplicação atual

O `golden.json` já possui schema e versão, 20 casos e categorias de resposta fundamentada, múltiplas evidências, ausência de evidência, conflito, citação, prompt injection e isolamento. A evolução recomendada é documentar a origem e a justificativa de cada caso, separar casos de desenvolvimento dos casos de validação e tornar a cobertura uma verificação automática em `load_dataset()` ou nos testes.

## 3. Baseline e regressão do retriever

### Objetivo

Uma execução isolada mostra o estado atual, mas não mostra se o resultado melhorou ou piorou em relação a uma versão anterior.

### Como implementar profissionalmente

Salvar, junto com cada execução, o conjunto de dados, thresholds, modelo de embedding, configuração de chunking, backend, scores agregados e resultados por caso. Comparar a execução atual com um baseline aprovado e classificar diferenças por impacto absoluto e relativo.

Uma regressão de segurança deve bloquear mesmo que Recall tenha melhorado. Uma melhoria de Recall não deve mascarar aumento de vazamento, latência ou resultados vazios.

### Como encaixar na aplicação atual

O projeto possui `evals/baseline.json` para a evaluation determinística geral, mas o fluxo de retrieval ainda não possui um baseline de ranking e não reprova automaticamente diferenças. Criar um baseline específico para retrieval, por exemplo com `Recall@1`, `Recall@3`, `Recall@5`, `MRR`, `nDCG`, isolamento e P95. O relatório atual já preserva casos, scores e diagnósticos, o que permite gerar a comparação sem mudar o contrato principal.

## 4. Automação e CI

### Objetivo

O fluxo precisa ser repetível por qualquer membro da equipe e executado automaticamente nos momentos em que uma mudança pode afetar o retrieval.

### Como implementar profissionalmente

Separar os níveis de validação:

1. validação rápida do schema e das métricas com dados controlados;
2. teste de integração com banco e embeddings controlados ou previamente armazenados;
3. evaluation real com o provider autorizado, executada em ambiente protegido;
4. gate de thresholds e publicação do relatório como artefato.

Fixar dependências, registrar o comando executado e evitar que uma falha de infraestrutura seja interpretada como zero de qualidade. A CI deve distinguir falha de código, falha de configuração, falha de provider e falha de qualidade.

### Como encaixar na aplicação atual

O `run_evaluation.sh` já oferece `test`, `real`, `--prepare`, `--ks`, filtros de métricas e `--debug`. O teste automatizado está em `tests/test_retrieval_evaluation.py`, mas a execução local sem o ambiente Docker falha quando `ranx` não está instalado, e não há um gate de CI visível no repositório. O próximo passo é usar o container como ambiente oficial, adicionar um job para o teste rápido e outro job controlado para a evaluation real, com thresholds e artefato JSON.

## 5. Reprodutibilidade e rastreabilidade

### Objetivo

Duas execuções precisam ser comparáveis. Para isso, não basta guardar apenas a média das métricas.

### Como implementar profissionalmente

Registrar no relatório:

- commit ou versão da aplicação;
- hash e versão do dataset;
- versão exata das dependências;
- modelo e dimensão do embedding;
- estratégia e configuração do vector store;
- parâmetros de chunking e overlap;
- valores de `k`;
- timestamp e ambiente da execução;
- identificador do corpus preparado.

Também é importante controlar mudanças de provider e modelo, pois a mesma pergunta pode produzir embeddings diferentes em versões distintas.

### Como encaixar na aplicação atual

O relatório atual já registra tipo da execução, dataset, versão, backend, coleção, modelo, `ks` e métricas operacionais. Ainda faltam commit, hash do dataset, dimensão, parâmetros de chunking, versão de dependências e identificador do ambiente. Esses campos podem ser adicionados ao objeto `run` em `report.py` sem alterar o cálculo das métricas.

## 6. Observabilidade, histórico e custo

### Objetivo

Uma evaluation profissional não termina quando imprime JSON. É necessário acompanhar tendência, custo, latência e causas de falha entre execuções.

### Como implementar profissionalmente

Persistir cada relatório como artefato imutável e, quando houver uma plataforma de observabilidade, enviar somente os metadados necessários. Manter gráficos de relevância, segurança, latência, erros, resultados vazios, quantidade de casos e custo de embeddings. Permitir comparação entre versões e alertar regressões relevantes.

Separar dados de avaliação de dados de produção e não enviar conteúdo sensível sem política explícita. O relatório deve permitir investigar um caso individual sem depender apenas de uma média agregada.

### Como encaixar na aplicação atual

O `report.py` já produz resumo, scores, falhas, casos, latência, erros e um contrato preparado para observabilidade. O README também registra que a integração com Langfuse é futura. A implementação incremental é salvar o JSON em CI, adicionar o custo e o identificador da execução e, depois, enviar apenas métricas e diagnósticos sanitizados ao Langfuse.

## 7. Validação do ambiente e das dependências

### Objetivo

Uma evaluation precisa provar se falhou por qualidade ou porque o ambiente não estava pronto. Dependência ausente, banco vazio, chave inválida e porta ocupada não podem parecer uma queda de Recall.

### Como implementar profissionalmente

Executar um preflight antes da avaliação, validando:

- dependências instaladas;
- versão de Python e pacotes;
- disponibilidade do banco;
- coleção correta;
- existência do corpus preparado;
- credenciais e modelo de embedding;
- compatibilidade dos parâmetros de dimensão;
- espaço e conectividade necessários.

Classificar a execução como `blocked` ou `infrastructure_error` quando o preflight falhar. Só calcular qualidade quando o retriever tiver executado todos os casos esperados.

### Como encaixar na aplicação atual

O fluxo atual usa `docker compose`, `evaluation-vector-db`, `--no-deps`, `DATABASE_URL`, `PGVECTOR_COLLECTION` e preparação explícita. O `run_evaluation.sh` pode ganhar uma etapa `preflight` que verifica dependências, banco e coleção antes de chamar `evaluate.py`. A documentação deve manter claro que `--prepare` é necessário quando o corpus ou o chunking mudar e que `--debug` é uma execução interativa, não um modo de CI.

## Fluxo profissional recomendado

```text
validar ambiente
→ validar schema e cobertura do dataset
→ preparar corpus isolado
→ executar retrieval com configuração registrada
→ calcular ranking, segurança e operação
→ comparar com thresholds e baseline
→ classificar passed, failed ou infrastructure_error
→ publicar relatório e artefatos
→ acompanhar tendência e custo
```

## Estado atual e limite de interpretação

O Rastro AI já possui uma base funcional sólida para evaluation de retrieval: dataset versionado, preparação de corpus, busca real com PGVector, métricas clássicas, invariantes de segurança, métricas operacionais, relatório estruturado, testes controlados e modo de debug.

No estado atual, a execução deve ser interpretada como **avaliação observacional e reproduzível em ambiente controlado**, não como um gate automático de qualidade. Thresholds, baseline de ranking, CI, governança formal do dataset, rastreabilidade completa e observabilidade histórica continuam sendo evoluções necessárias para declarar maturidade operacional.
