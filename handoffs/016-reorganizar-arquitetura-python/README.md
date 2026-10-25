# 016 — Reorganizar arquitetura do serviço Python
- Data/hora: 2026-10-25 -03:00 | Status: `verified`; aplicação: IA (`rastro-ai`).
- Objetivo: reduzir sobreposição entre módulos e preparar composição, orquestração e evaluation evolutivas.
- Dependência/ordem: `015` verificada; `016` inicia a sequência pela composição explícita, sem remoções históricas.
- Impacto: importação das fachadas deixa de construir vector store; contratos e fluxo de indexação permanecem compatíveis.
- Evolução: `v1` criou containers explícitos; `v2` removeu aliases internos sem consumidores e o provider Sentence Transformer não utilizado.
- Pendências: separar workflows e reorganizar evaluation nas próximas etapas; consumidores externos dos aliases removidos precisam migrar.
- Pasta: `handoffs/016-reorganizar-arquitetura-python/`; próxima ação: iniciar `017-consolidar-namespaces-python`.
