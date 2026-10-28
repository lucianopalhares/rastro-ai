# 027/v6 — Documentação do fluxo e escolha de métricas

- Versão-base: `v5` aplicada; `docs/rag-evaluation-flow.md` e `rastro-ai/evals/retrieval/README.md` foram conferidos.
- Estado encontrado: a documentação explicava métricas básicas, mas não mostrava por setas o fluxo completo nem que a escolha depende do projeto.
- Escopo autorizado: atualizar a documentação em `docs/` com fluxo, categorias, critérios de escolha e limites entre retriever, contexto e resposta.
- Invariante: não adicionar métricas ao runtime; o conjunto atual do Rastro AI permanece Recall, Precision, MRR, nDCG e invariantes.

## O que foi feito

Atualizado `/home/dev/dev/ia/rastro-ai/docs/rag-evaluation-flow.md` com setas do fluxo completo, tabela de escolha de métricas, ordem de aplicabilidade, regras para decidir quando usar ou não cada métrica, interpretação por projeto, opções futuras de diversidade, reranking, robustez, operação e saúde da base, além da separação entre retriever, contexto e resposta.

## O que muda na aplicação

Não há mudança de runtime. A documentação passa a deixar claro que nem todas as métricas devem ser usadas em todos os projetos e que `ranking_metrics`, invariantes, avaliação contextual e evaluation de resposta são camadas diferentes. O arquivo está sob `docs/*` no `.gitignore`, portanto permanece uma alteração local documentada e não será incluído automaticamente em commit.

## Jornada da aplicação nesta versão

Antes, a documentação listava métricas e ferramentas; agora conecta cada métrica a uma pergunta, mostra o fluxo por etapas, define a ordem de decisão, explica pré-condições do golden e indica quando uma extensão deve ou não ser aplicada. O resultado é uma orientação de estudo e decisão para o retriever sem misturar qualidade da resposta do LLM.

## Como usar e validar a aplicação nesta versão

Leia `docs/rag-evaluation-flow.md` seguindo as setas das seções 2, 3, 5 e 7. Compare a seção 5 com `rastro-ai/evals/retrieval/README.md` para verificar que o conjunto atualmente implementado continua separado das possibilidades futuras.

## Cobertura por comportamento

- Fluxo visual: `docs/rag-evaluation-flow.md`; evidência de contrato: comando `rg` da validação; esperado: etapas do retriever, contexto, resposta e operação conectadas por setas.
- Escolha de métricas: seção 3; evidência de contrato: tabela, árvore de decisão, ordem de aplicabilidade e regras por métrica conferidas pelo mesmo comando; esperado: cada grupo explica quando usar, quando não usar e como interpretar.
- Fronteira entre evaluations: seção 5; evidência de contrato: seção localizada pelo comando; esperado: retriever, contexto e resposta permanecem separados.
- Runtime: não alterado; testes de código não são necessários para esta rodada documental e a validação integrada não se aplica.

## Instruções de validação

```bash
rg -n "^## |↓|ranking_metrics|invariants|não.*todas|Reranking|resposta" docs/rag-evaluation-flow.md
```

Resultado esperado: o documento contém as seções, setas, separação entre grupos, árvore de decisão, ordem de aplicabilidade e orientação de escolha.

```bash
git diff --check
```

Resultado esperado: nenhuma falha de whitespace. Como `docs/` é ignorado pelo Git, confirme o conteúdo diretamente no caminho real.
