# Timeline — 027/v7 HitRate e operação

## 2026-10-28 00:45 -03:00 — aplicação da v7

- Status: `applied`.
- Arquivos reais alterados: `evaluate.py`, adapter ranx, `report.py`, testes, README de retrieval e documentação do fluxo.
- Mudanças: `HitRate@k`, latência média/P95, taxa de erro, taxa de resultado vazio e registro de erro por caso.
- Decisão: erro técnico não conta como abstention; `ranx` recebe zero quando a lista recuperada está vazia.
- Verificação: compilação, diff e suíte controlada concluídos; 7 testes terminaram com `OK`.
- Limite: evaluation real contra PGVector e thresholds de produção não executados; finalização aguarda comando explícito.
