# 013 — Configurar debug do Python e da API no VS Code
- Data/hora: 2026-10-24 -03:00 | Status: `verified` | Aplicação: raiz, API e IA.
- Objetivo: permitir breakpoints simultâneos no serviço Python e na API NestJS.
- Dependência/ordem: construir e iniciar `api`, `ai-indexer` e `vector-db` pelo Compose; depois conectar o compound Docker do VS Code.
- Motivo: reduzir o tempo de diagnóstico no fluxo HTTP API → indexador Python.
- Impacto: adiciona debug Docker, `debugpy`, inspector NestJS e comandos reproduzíveis; produção permanece inalterada.
- Critério: imagens Docker construídas, portas `9229`/`5678` publicadas, requests API/Python aprovados e instruções de attach registradas.
- Evolução: `v1` criou debug local; `v2` ajustou o debug para Docker; `v3` documentou o upload do fixture no README da API; `v4` adiciona `multer`; `v7` corrige o comando `curl` para usar `@`; `v8` documenta a indexação direta no Python; `v9` consolida o fluxo na raiz; `v10` documenta a delegação API → Python e suas variáveis.
- Pasta: `handoffs/013-configurar-debug-python-api-vscode/` | Próxima ação: nenhuma; attach visual no VS Code permanece opcional/manual.
