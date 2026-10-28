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
MODE="${1:-}"

if [[ "$MODE" == "test" || "$MODE" == "real" ]]; then
  shift
fi

# Mostra as opções para reduzir a necessidade de copiar o comando Docker completo.
show_help() {
  cat <<'EOF'
Uso: run_evaluation.sh test
     run_evaluation.sh real [--prepare] [--ks VALORES]

Executa o teste automatizado ou a avaliação real do retriever.

Modos:
  test            Executa testes controlados sem banco, OpenAI ou documentos reais.
  real            Consulta o banco PostgreSQL/PGVector de evaluation.

Opções:
  --prepare       Reindexa o corpus do golden antes de avaliar.
  --ks VALORES    Valores de k separados por vírgula. Padrão: 1,3,5.
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
    --ks)
      if (($# < 2)); then
        echo "--ks exige valores separados por vírgula" >&2
        exit 2
      fi
      KS="$2"
      shift 2
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
  ai-indexer
)

if [[ "$PREPARE" == true ]]; then
  # Só gera embeddings novamente quando o usuário pede explicitamente a preparação.
  "${COMPOSE[@]}" "${COMMON_ARGS[@]}" \
    python -m evals.retrieval.prepare \
    --dataset "$DATASET_PATH"
fi

# Consulta o retriever real e imprime o JSON detalhado da evaluation.
"${COMPOSE[@]}" "${COMMON_ARGS[@]}" \
  python -m evals.retrieval.evaluate \
  --dataset "$DATASET_PATH" \
  --ks "$KS"
