# Timeline — 024/v1 Langfuse self-hosted e observabilidade da indexação

## 2026-10-26 -03:00 — planejamento v1
- Status: `proposed`.
- Arquivos reais conferidos: `docker-compose.yml`, `.env.example`, `rastro-ai/pyproject.toml`, indexação, embeddings, testes e README.
- Decisão: stack em Compose complementar, UI externa `38917`, instrumentação opcional e payload sanitizado.
- Pendência: aplicar arquivos reais, instalar SDK no container, validar smoke e atualizar status.

## 2026-10-26 -03:00 — aplicação v1

- Status: `applied`.
- Arquivos reais conferidos: `docker-compose.langfuse.yml`, `docker-compose.yml`, `.env.example`, `README.md`, `rastro-ai/pyproject.toml`, Dockerfiles, boundary de observabilidade, indexação, embeddings e testes.
- Mudanças aplicadas: stack self-hosted com portas externas `38917`, `38918` e `38919`; SDK `langfuse>=5,<6`; traces sanitizados para indexação e embeddings; isolamento de falhas de telemetria; documentação e testes.
- Problema resolvido: ausência de observabilidade operacional da indexação sem enviar conteúdo documental ao Langfuse.
- Evidência: Compose válido; serviços Langfuse healthy; health HTTP 200; imagem `ai-indexer` construída; 36 testes Python executados no container; health do indexador HTTP 200; `git diff --check` aprovado.
- Pendência: trace autenticado ainda depende da criação manual de projeto/chaves na UI e da habilitação explícita da flag.

## 2026-10-26 -03:00 — verificação e finalização v1

- Status: `verified`.
- Evidência adicional: usuário confirmou trace da chamada `POST http://127.0.0.1:18473/index` no painel Langfuse; observação exibiu status `DEFAULT` e custo vazio conforme a instrumentação atual.
- Verificações finais: 36 testes Python no container, Compose válido, serviços healthy, health HTTP 200 do Langfuse e indexador, `git diff --check` e hook estrutural aprovados.
- Limitação registrada: custo não é calculado porque usage/tarifação do embedding não foram instrumentados; isso fica fora do escopo da implementação.
- Commit: `73fffe7` — `adiciona observabilidade Langfuse na indexação`.
