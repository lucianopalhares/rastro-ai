#!/usr/bin/env bash

set -euo pipefail

# Encaminha o comando da raiz para a implementação única do módulo de retrieval.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/rastro-ai/evals/retrieval/run_evaluation.sh" "$@"
