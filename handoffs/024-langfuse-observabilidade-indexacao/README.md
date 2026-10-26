# 024 — Langfuse para observabilidade da indexação
- Data/hora: 2026-10-26 -03:00 | Status: `verified`; aplicação: `rastro-ai` e raiz.
- Objetivo: adicionar Langfuse self-hosted e traces seguros ao fluxo de indexação Python.
- Dependência/ordem: `023` verificada; stack local subiu antes do smoke de observabilidade.
- Evolução: `v1` criou Compose isolado, SDK opcional e observações de indexação/embeddings sem mudar o runtime funcional.
- Decisão/invariante: Langfuse é desligável; documentos completos e textos de chunks não são enviados aos traces.
- Impacto: stack local adicional; falhas de telemetria não alteram o fallback da indexação.
- Evidência: UI/health HTTP 200, trace autenticado visualizado, 36 testes no container, health do indexador e hook aprovados; custo permanece sem usage/preço configurado.
- Pasta/próxima ação: `handoffs/024-langfuse-observabilidade-indexacao/`; tarefa encerrada, próxima iniciativa pode ser iniciada.
