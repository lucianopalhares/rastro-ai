# Fluxo de avaliação de RAG

Este documento separa o que pertence ao retriever, ao contexto entregue ao modelo e à resposta final. A regra principal é não aplicar todas as métricas automaticamente: cada uma deve responder a um risco ou objetivo do projeto.

## 1. Defina o que é uma recuperação correta

Para cada pergunta, registre:

- os documentos ou chunks relevantes;
- o grau de relevância, quando necessário;
- quais evidências são obrigatórias;
- se a pergunta não possui evidência suficiente e deve gerar abstinência.

Esse conjunto é o `golden dataset` ou `qrels`. Sem julgamentos confiáveis, as métricas não representam a qualidade real.

## 2. Separe as etapas avaliadas

```text
pergunta
  ↓
normalização da consulta
  ↓
embedding da consulta
  ↓
busca de candidatos
  ↓
filtros de projeto e permissão
  ↓
reranking, quando existir
  ↓
remoção de duplicados e seleção do top-k
  ↓
contexto entregue ao modelo
  ↓
resposta e citações
  ↓
latência, custo, erros e regressões em produção
```

O retriever deve ser avaliado separadamente da resposta gerada. As métricas de retrieval observam principalmente os resultados recuperados e selecionados; elas não medem sozinhas a qualidade do LLM.

## 3. Avalie o ranking do retriever

Use métricas clássicas de Information Retrieval somente quando elas responderem a uma pergunta importante do projeto:

- `Recall@k`: quantas evidências relevantes apareceram no top-k;
- `Precision@k`: quanto do top-k é relevante;
- `Hit@k`: se apareceu pelo menos uma evidência relevante;
- `MRR`: posição da primeira evidência relevante;
- `MAP`: precisão acumulada ao longo do ranking;
- `nDCG@k`: qualidade da ordem, especialmente com relevância graduada;
- `R-Precision`: precisão considerando a quantidade conhecida de evidências relevantes.

| Métrica | Pergunta que responde | Use quando |
| --- | --- | --- |
| `Recall@k` | Encontramos todas as evidências necessárias? | Não pode faltar informação relevante. |
| `Precision@k` | Quanto do top-k realmente ajuda? | O contexto tem limite ou ruído prejudica. |
| `Hit@k` | Apareceu pelo menos uma evidência? | Uma evidência inicial já é útil. |
| `MRR` | A primeira evidência aparece cedo? | A primeira evidência tem grande valor. |
| `MAP@k` | Várias evidências aparecem ao longo da lista? | Existem múltiplos acertos relevantes. |
| `nDCG@k` | As evidências mais importantes estão no começo? | Há relevância graduada ou prioridades. |
| `R-Precision` | A lista recuperou uma proporção adequada? | O número esperado de relevantes é conhecido. |

Use `Recall@k` e `Hit@k` quando não pode faltar evidência. Use `Precision@k` quando o contexto tem limite e ruído prejudica a resposta. Use `MRR` quando a primeira evidência é suficiente. Use `nDCG` quando a ordem e diferentes graus de relevância importam. Não é necessário usar todas: métricas redundantes tornam o diagnóstico mais difícil.

### Como decidir se uma métrica pode ser usada

Antes de calcular uma métrica, aplique estas regras ao projeto e ao golden dataset:

```text
1. Existe um gabarito confiável de evidências?
   ├── não → não interpretar a métrica; revisar o golden
   └── sim
       ↓
2. A pergunta tem evidência esperada ou é um caso sem resposta?
   ├── sem evidência → usar abstention e não interpretar MRR como acerto
   └── com evidência
       ↓
3. Uma evidência perdida é um risco grave?
   ├── sim → Recall@k e Hit@k
   └── não
       ↓
4. O contexto tem limite ou o ruído prejudica o modelo?
   ├── sim → Precision@k
   └── não
       ↓
5. A primeira evidência basta ou precisa aparecer cedo?
   ├── sim → MRR
   └── não
       ↓
6. Existem graus diferentes de importância entre as evidências?
   ├── sim → nDCG@k
   └── não → não adicionar nDCG apenas por padrão
```

Uma métrica pode ser calculada tecnicamente e ainda assim não ser válida para a decisão do projeto. Se o golden não registra todos os chunks relevantes, por exemplo, Recall baixo pode significar apenas que o gabarito está incompleto.

### Ordem recomendada de aplicabilidade

Esta é a ordem de decisão, não uma obrigação de implementar todas as métricas:

```text
pré-condições do golden
  ↓
invariantes de segurança e consistência
  ↓
Hit@k / Recall@k
  ↓
Precision@k
  ↓
MRR
  ↓
nDCG@k
  ↓
MAP@k / R-Precision, se várias evidências forem necessárias
  ↓
diversidade, robustez, latência e custo, conforme o risco operacional
```

As invariantes vêm antes porque não faz sentido comemorar um bom Recall se a busca trouxe dados de outro projeto ou se os scores estão inválidos. `Hit@k` e `Recall@k` verificam primeiro se a informação chegou; `Precision@k` verifica o ruído; `MRR` e `nDCG@k` analisam a posição e a importância dos resultados; as métricas operacionais verificam se a solução é utilizável.

### Regras por métrica

| Métrica | Pode usar quando | Não usar ou não interpretar quando | Como interpretar |
| --- | --- | --- | --- |
| `Recall@k` | O golden lista todas as evidências necessárias e faltar uma é relevante. | O golden é parcial ou o projeto aceita respostas com qualquer evidência suficiente. | Baixo indica evidência faltando no top-k; compare k diferentes para descobrir o limite necessário. |
| `Precision@k` | O contexto tem tamanho limitado e chunks inúteis atrapalham. | O retriever ainda não tem julgamentos de relevância confiáveis. | Baixo indica ruído; investigue se o problema é embedding, filtro, chunking ou k excessivo. |
| `Hit@k` | Uma única evidência correta já permite prosseguir. | A resposta depende de todas as evidências obrigatórias. | `1` significa que ao menos uma evidência apareceu; não prova que o conjunto está completo. |
| `MRR` | A primeira evidência correta tem prioridade e o restante é secundário. | A resposta precisa combinar muitos chunks relevantes. | Baixo indica que o primeiro acerto aparece tarde; não informa se todas as evidências foram encontradas. |
| `nDCG@k` | O golden atribui graus de relevância ou há uma ordem de importância. | Todos os chunks relevantes têm o mesmo peso ou o golden não registra esses pesos. | Baixo indica que itens importantes estão abaixo de itens menos úteis. |
| `MAP@k` | Existem vários itens relevantes e cada acerto ao longo da lista importa. | Há somente um item relevante por pergunta ou a relevância é graduada. | Baixo indica que os acertos estão escassos ou muito espalhados no ranking. |
| `R-Precision` | O número de relevantes esperados é conhecido por pergunta. | O número de relevantes é incerto ou o golden é incompleto. | Compara a precisão até a quantidade esperada de evidências. |
| `Diversity` | Fontes ou documentos diferentes precisam complementar a resposta. | Repetições do mesmo documento são desejáveis ou a fonte única é suficiente. | Baixa diversidade indica concentração; não significa automaticamente baixa relevância. |
| `Latency` e `Cost` | O retriever será usado em produção ou há limite operacional. | Apenas um teste unitário isolado está sendo validado. | Um ranking melhor pode não ser aceitável se ultrapassar o orçamento de tempo ou custo. |

### Como interpretar os valores

Não existe um valor universal que determine que um retriever está bom. Interprete sempre nesta ordem:

```text
valor da métrica
  ↓
qualidade do golden
  ↓
tipo de pergunta
  ↓
k utilizado
  ↓
baseline ou versão anterior
  ↓
limite definido pelo produto
  ↓
decisão de melhoria
```

Um `Recall@5 = 0,8` pode ser bom para uma busca exploratória e ruim para uma consulta jurídica em que toda evidência é obrigatória. Da mesma forma, `Precision@5 = 0,6` pode ser aceitável se o modelo tolera ruído, mas inadequado se o contexto tem poucos tokens.

Registre para cada métrica: objetivo, conjunto de consultas ao qual se aplica, valor de `k`, baseline, limite esperado e ação quando falhar. Nunca altere o retriever para melhorar um número sem confirmar que o comportamento real do projeto melhorou.

[`ranx`](https://amenra.github.io/ranx/metrics/) ou [`pytrec_eval`](https://github.com/cvangysel/pytrec_eval) devem ser preferidos para essas métricas em vez de manter implementações próprias. `ranx` prioriza integração Python; `pytrec_eval` é uma interface para métricas tradicionais do `trec_eval`.

### Outras métricas possíveis do retriever

As métricas clássicas não cobrem todos os problemas. Escolha extensões somente quando houver uma necessidade clara:

```text
risco do projeto
  ↓
pergunta que precisa ser respondida
  ↓
métrica adequada
  ↓
limite esperado
  ↓
decisão sobre o retriever
```

- **Diversidade e redundância:** chunks duplicados, documentos únicos, cobertura de fontes e repetição de conteúdo. São úteis quando três chunks do mesmo documento podem ser piores que três fontes complementares.
- **Reranking:** compare `Recall@k`, `MRR`, `nDCG@k`, latência e custo antes e depois do reranker. O reranker deve demonstrar ganho compatível com o custo adicional.
- **Robustez:** estabilidade com paráfrases, abreviações, erros de digitação, perguntas curtas e consultas em idiomas diferentes.
- **Operação:** latência média, P95/P99, taxa de erro, consultas sem resultado, custo de embedding, custo do reranker e quantidade de tokens enviada ao contexto.
- **Saúde da base:** documentos desatualizados, chunks duplicados, chunks sem metadata ou embedding e documentos indexados que nunca são recuperados.

Essas medidas complementam Recall e nDCG; não devem ser adicionadas apenas por serem conhecidas no mercado.

### Invariantes e regras do produto

Além das métricas genéricas, preserve verificações próprias para regras que não são ranking:

```text
resultado recuperado
  ↓
project_isolation → não houve vazamento entre projetos
  ↓
score_ordering → os scores estão em ordem decrescente
  ↓
abstention → consultas sem evidência não trouxeram ruído
```

Essas verificações pertencem ao retriever, mas devem permanecer separadas das `ranking_metrics`. Elas não representam uma etapa de reranking.

## 4. Avalie o contexto recuperado

Métricas clássicas usam julgamentos explícitos. Para avaliar suficiência e relevância semântica do contexto, use uma ferramenta como Ragas ou DeepEval:

- `Context Recall`: o contexto contém toda a informação necessária?
- `Context Precision`: os chunks úteis estão acima do ruído?
- `Context Relevancy`: o contexto é realmente relacionado à pergunta?
- `Noise Sensitivity`: a resposta é afetada por contexto irrelevante?

Essas métricas normalmente usam LLM-as-a-judge. Elas têm custo e variabilidade, portanto complementam — não substituem — as métricas determinísticas. Consulte as métricas disponíveis no [`Ragas`](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) e no [`DeepEval`](https://deepeval.com/guides/guides-rag-evaluation).

## 5. Avalie a resposta separadamente

Depois do retriever, avalie:

- correção da resposta;
- completude;
- fidelidade ao contexto (`faithfulness`);
- relevância da resposta;
- precisão das citações;
- abstinência quando não há evidência.

Não use uma boa resposta final para esconder um retriever ruim: uma resposta pode parecer correta mesmo quando a recuperação falha, e o modelo pode compensar ou inventar informação.

## 6. Mantenha regras específicas do produto

Além das bibliotecas, preserve verificações próprias para regras que não são métricas genéricas de ranking:

- isolamento entre projetos ou tenants;
- ordenação e sentido dos scores;
- limites de `k`;
- ausência de resultados sem evidência;
- formato e consistência do golden dataset.

## 7. Fluxo recomendado

```text
1. criar e revisar o golden dataset
   ↓
2. definir riscos do projeto e métricas necessárias
   ↓
3. testar o cálculo com dados controlados
   ↓
4. executar o retriever real
   ↓
5. medir ranking, invariantes e, quando aplicável, diversidade
   ↓
6. comparar candidatos antes/depois do reranking
   ↓
7. medir contexto e resposta em avaliações separadas
   ↓
8. acompanhar custo, latência, erros e regressões em produção
```

No Rastro AI, `HitRate@k`, `Recall@k`, `Precision@k`, `MRR`, `nDCG@k`, `project_isolation`, `score_ordering` e `abstention` formam a base atual. A evaluation também registra latência média/P95, taxa de erro e taxa de resultado vazio. `MAP`, `R-Precision`, diversidade, robustez e avaliação contextual são possibilidades futuras, não requisitos automáticos.

## 8. Como executar uma análise curta ou detalhada

```text
comando real
  ↓
retrieval completo
  ↓
seleção da apresentação
  ├── --summary → métricas agregadas
  ├── --only-failures → resumo + casos falhos
  └── sem filtro → relatório completo
        ↓
seleção opcional de métricas
  ├── --metrics ranking
  ├── --metrics invariants
  ├── --metrics operational
  └── --metrics recall@3,precision@3
```

Exemplos:

```bash
./run_evaluation.sh real --summary
./run_evaluation.sh real --only-failures
./run_evaluation.sh real --summary --metrics ranking
./run_evaluation.sh real --summary --metrics recall@3,precision@3,ndcg@3
```

O filtro `--metrics` reduz as métricas exibidas no relatório. As invariantes continuam sendo executadas internamente mesmo quando outro grupo é selecionado, porque segurança e consistência não devem ser ocultadas por um filtro de apresentação.
