# Timeline — 025/v1 tokens e custos de embeddings no Langfuse

## 2026-10-26 -03:00 — planejamento v1

- Status: `proposed`.
- Arquivos reais conferidos: boundary de observabilidade, repositório OpenAI/LangChain, testes, `pyproject.toml`, `.env.example`, `docker-compose.yml` e README.
- Decisão: usar `model` top-level, contar tokens localmente, enviar usage e permitir custo direto opcional sem hardcode de preço.
- Mudanças aplicadas: observability aceita modelo top-level; repository conta tokens com `tiktoken`, envia usage e custo direto opcional; configuração e README foram atualizados; testes cobrem uso/custo sem rede.
- Evidência inicial: imagem construída, 37 testes Python aprovados, Compose válido, indexação real HTTP 200 e health do indexador aprovado.
- Pendência: confirmar visualmente no painel os campos de usage/cost; o endpoint público de observações testado respondeu HTTP 404 no Langfuse v4 local.

## 2026-10-26 -03:00 — finalização solicitada

- Status: `applied` (não verificado).
- Evidência: código aplicado, 37 testes Python aprovados, Compose válido, imagem construída e indexação real HTTP 200; tokens foram observados no painel.
- Pendência bloqueadora: custo não apareceu no trace novo; é necessário corrigir ou confirmar o matching da definição `text-embedding-3-small`/preço `input`, ou validar o custo direto por ambiente.
- Decisão: manter `CURRENT.md` em `025`, não avançar a sequência e não gerar commit automático enquanto a pendência de custo permanecer.
- Commit de checkpoint: `f27c389` — `adiciona tokens e custos ao tracing de embeddings`.

## 2026-10-27 -03:00 — tentativa de finalização

- Status: `applied` (permanece não verificado).
- Arquivos reais conferidos: observabilidade, repository de embeddings, testes, Compose e handoffs da 025.
- Evidência: cinco testes específicos passaram no container e o hook estrutural validou os quatro arquivos de handoff.
- Limites: teste completo no container encontrou `evals` fora do `PYTHONPATH`; execução local não possui dependências Python; custo inferido não foi confirmado no painel Langfuse.
- Decisão: manter a tarefa ativa, sem `verified`, sem avanço de `CURRENT.md` e sem commit automático.

## 2026-10-27 -03:00 — finalização

- Status: `verified`.
- Evidência: 41 testes Python passaram no container, Compose válido e hook estrutural aprovado.
- Integração: usuário confirmou tokens e custo no trace após configurar o custo direto por token.
- Resultado: a observação de embedding expõe modelo, usage e custo sem conteúdo textual; o runtime de indexação permanece preservado.
- Controle: `CURRENT.md` voltou a `idle`; não há pendências da versão.
