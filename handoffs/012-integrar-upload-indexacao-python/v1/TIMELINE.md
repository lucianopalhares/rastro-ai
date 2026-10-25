# Linha do tempo — 012/v1 Contrato e integração do upload com a indexação Python

## v1 — Registro inicial

- Data/hora: 2026-10-24 -03:00 | Status: `proposed`.
- Arquivos reais conferidos: API de documentos e módulos de indexação/retrieval Python.
- Mudanças aplicadas: criação do README da versão e ativação da implementação 012; nenhum arquivo de runtime foi alterado.
- Problema resolvido: objetivo, dependências, limites e critérios da integração foram registrados para a próxima rodada.
- Pendências: escolher transporte, worker, contrato de eventos ou HTTP, retry, idempotência e observabilidade.
- Verificação: hook estrutural, consistência do `CURRENT.md` e inspeção da árvore de handoffs.

## v1 — Implementação e smoke ponta a ponta

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: gateway e caso de uso de upload da API, módulo de documentos, serviço HTTP Python, fachada de indexação, Compose e testes.
- Mudanças aplicadas: POST JSON API → Python, endpoint `/health`/`/index`, persistência dos chunks e estados `processing`, `ready` e `failed`.
- Verificação real: API com 10 testes/build, Python com 23 testes/compilação, Compose e hook aprovados; upload multipart real retornou `status: "ready"`.
- Ambiente: publicação externa do indexador usa `18000` por padrão para evitar conflito com serviços locais que usam `8000`.
- Pendências: retry, idempotência explícita, processamento assíncrono e validação com pgvector real permanecem para evolução posterior.
