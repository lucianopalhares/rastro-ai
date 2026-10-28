#!/usr/bin/env bash

set -euo pipefail

# Localiza a raiz para que o script funcione mesmo quando chamado fora dela.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPOSITORY_ROOT="$(cd -- "$SCRIPT_DIR/../../.." && pwd)"
DATASET_PATH="/app/evals/dataset/golden.json"
DATABASE_URL="postgresql://rastro:rastro@evaluation-vector-db:5432/rastro_evaluation"
PGVECTOR_COLLECTION="rastro_document_chunks"
KS="${EVAL_KS:-1,3,5}"
PREPARE=false
SUMMARY=false
ONLY_FAILURES=false
METRICS="all"
DEBUG=false
DEBUG_PORT="${EVAL_DEBUG_PORT:-5678}"
MODE="${1:-}"

if [[ "$MODE" == "test" || "$MODE" == "real" ]]; then
  shift
fi

# Mostra as opções para reduzir a necessidade de copiar o comando Docker completo.
show_help() {
  cat <<'EOF'
Uso: run_evaluation.sh test
     run_evaluation.sh real [--prepare] [--debug] [--ks VALORES] [--metrics SELEÇÃO]

Executa o teste automatizado ou a avaliação real do retriever.

Modos:
  test            Executa testes controlados sem banco, OpenAI ou documentos reais.
  real            Consulta o banco PostgreSQL/PGVector de evaluation.

Opções:
  --prepare       Reindexa o corpus do golden antes de avaliar.
  --debug         Aguarda o VS Code conectar via debugpy antes de executar a avaliação.
  --ks VALORES    Valores de k separados por vírgula. Padrão: 1,3,5.
  --metrics VALOR all, ranking, invariants, operational ou nomes separados por vírgula.
  --summary       Imprime somente o resumo agregado, sem os casos detalhados.
  --only-failures Imprime o resumo e somente os casos com falha.
  -h, --help      Mostra esta ajuda.
EOF
}

# Lê apenas opções do script e impede argumentos silenciosamente ignorados.
while (($# > 0)); do
  case "$1" in
    --prepare)
      PREPARE=true
      shift
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    --ks)
      if (($# < 2)); then
        echo "--ks exige valores separados por vírgula" >&2
        exit 2
      fi
      KS="$2"
      shift 2
      ;;
    --metrics)
      if (($# < 2)); then
        echo "--metrics exige um grupo ou nomes separados por vírgula" >&2
        exit 2
      fi
      METRICS="$2"
      shift 2
      ;;
    --summary)
      SUMMARY=true
      shift
      ;;
    --only-failures)
      ONLY_FAILURES=true
      shift
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo "Opção desconhecida: $1" >&2
      show_help >&2
      exit 2
      ;;
  esac
done

if [[ "$SUMMARY" == true && "$ONLY_FAILURES" == true ]]; then
  echo "--summary e --only-failures não podem ser usados juntos" >&2
  exit 2
fi

if [[ "$MODE" != "test" && "$MODE" != "real" ]]; then
  echo "Informe o modo: test ou real" >&2
  show_help >&2
  exit 2
fi

COMPOSE=(
  docker compose
  -f "$REPOSITORY_ROOT/docker-compose.yml"
  -f "$REPOSITORY_ROOT/docker-compose.langfuse.yml"
)

if [[ "$MODE" == "test" ]]; then
  # Executa somente métricas e orquestração com resultados controlados.
  "${COMPOSE[@]}" run --rm --no-deps \
    -e PYTHONPATH=/app:/app/src \
    -v "$REPOSITORY_ROOT/rastro-ai/tests:/app/tests:ro" \
    -v "$REPOSITORY_ROOT/rastro-ai/evals:/app/evals:ro" \
    ai-indexer \
    python -m unittest -q tests.test_retrieval_evaluation
  exit 0
fi

# Garante que o banco exclusivo esteja disponível antes dos containers temporários.
"${COMPOSE[@]}" up -d --wait evaluation-vector-db

COMMON_ARGS=(
  run --rm --no-deps
  -e PYTHONPATH=/app:/app/src
  -e DATABASE_URL="$DATABASE_URL"
  -e PGVECTOR_COLLECTION="$PGVECTOR_COLLECTION"
  -v "$REPOSITORY_ROOT/rastro-ai/evals:/app/evals:ro"
)

if [[ "$DEBUG" == true ]]; then
  # Publica a porta do container temporário para o perfil de attach do VS Code.
  COMMON_ARGS+=( -p "$DEBUG_PORT:5678" )
fi
COMMON_ARGS+=( ai-indexer )

if [[ "$PREPARE" == true ]]; then
  # Só gera embeddings novamente quando o usuário pede explicitamente a preparação.
  "${COMPOSE[@]}" "${COMMON_ARGS[@]}" \
    python -m evals.retrieval.prepare \
    --dataset "$DATASET_PATH"
fi

# Consulta o retriever real e imprime o JSON detalhado da evaluation.
REPORT_ARGS=(
  --dataset "$DATASET_PATH"
  --ks "$KS"
  --metrics "$METRICS"
)
if [[ "$SUMMARY" == true ]]; then
  REPORT_ARGS+=(--summary)
elif [[ "$ONLY_FAILURES" == true ]]; then
  REPORT_ARGS+=(--only-failures)
fi

if [[ "$DEBUG" == true ]]; then
  # Mantém o processo parado até o VS Code anexar, para que breakpoints sejam respeitados.
  echo "Evaluation aguardando o VS Code na porta ${DEBUG_PORT}; execute 'Docker: Python AI service' agora." >&2
  "${COMPOSE[@]}" "${COMMON_ARGS[@]}" \
    python -Xfrozen_modules=off -m debugpy --listen 0.0.0.0:5678 --wait-for-client \
    -m evals.retrieval.evaluate \
    "${REPORT_ARGS[@]}"
else
  "${COMPOSE[@]}" "${COMMON_ARGS[@]}" \
    python -m evals.retrieval.evaluate \
    "${REPORT_ARGS[@]}"
fi
