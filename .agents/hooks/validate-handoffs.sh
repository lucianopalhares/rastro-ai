#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_FILE="$ROOT_DIR/AGENTS.md"

fail() {
  printf 'handoff validation failed: %s\n' "$1" >&2
  exit 1
}

[[ -f "$AGENTS_FILE" ]] || fail "AGENTS.md não foi encontrado"

while IFS= read -r application_line; do
  application_path="${application_line#*: }"
  application_path="${application_path//\`/}"
  [[ "$application_path" != "definir-caminho-real" ]] || fail "o caminho real da aplicação ainda está como definir-caminho-real em AGENTS.md"
  [[ -e "$ROOT_DIR/$application_path" ]] || fail "o caminho da aplicação não existe: $application_path"
done < <(sed -n -E '/^- (API|Frontend|IA|Raiz do projeto): /p' "$AGENTS_FILE")

if [[ "$#" -eq 0 ]]; then
  if git -C "$ROOT_DIR" rev-parse --show-toplevel >/dev/null 2>&1; then
    mapfile -t handoff_files < <(
      git -C "$ROOT_DIR" diff --cached --name-only --diff-filter=ACMR -- 'handoffs/*/README.md' 'handoffs/*/TIMELINE.md' 'handoffs/*/v[0-9]*/README.md' 'handoffs/*/v[0-9]*/TIMELINE.md'
    )
  else
    fail "passe os arquivos de handoff como argumentos quando o projeto não estiver em um repositório Git"
  fi
else
  handoff_files=("$@")
fi

[[ "${#handoff_files[@]}" -gt 0 ]] || exit 0

for relative_file in "${handoff_files[@]}"; do
  file_path="$ROOT_DIR/${relative_file#./}"
  [[ -f "$file_path" ]] || fail "arquivo de handoff não encontrado: $relative_file"

  case "$relative_file" in
    handoffs/*/README.md|handoffs/*/TIMELINE.md|handoffs/*/v[0-9]*/README.md|handoffs/*/v[0-9]*/TIMELINE.md) ;;
    *) fail "arquivo de controle fora do formato README.md/TIMELINE.md: $relative_file" ;;
  esac

  file_name="$(basename "$file_path")"
  [[ "$file_name" != *.handoff.md ]] || fail "$relative_file usa um sufixo que não pertence ao arquivo original"
  [[ -s "$file_path" ]] || fail "$relative_file está vazio"
done

printf 'handoffs válidos: %s arquivo(s)\n' "${#handoff_files[@]}"
