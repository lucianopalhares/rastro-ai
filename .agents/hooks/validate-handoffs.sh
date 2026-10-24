#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENTS_FILE="$ROOT_DIR/AGENTS.md"
REQUIRE_BEHAVIOR_COVERAGE="${REQUIRE_BEHAVIOR_COVERAGE:-0}"

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

  if [[ "$REQUIRE_BEHAVIOR_COVERAGE" == "1" && "$relative_file" == handoffs/*/v[0-9]*/README.md ]]; then
    grep -q '^## Cobertura por comportamento$' "$file_path" \
      || fail "$relative_file não possui a seção ## Cobertura por comportamento"
    grep -q '^## Jornada da aplicação nesta versão$' "$file_path" \
      || fail "$relative_file não possui a seção ## Jornada da aplicação nesta versão"
    grep -q '^## Como usar e validar a aplicação nesta versão$' "$file_path" \
      || fail "$relative_file não possui a seção ## Como usar e validar a aplicação nesta versão"
    grep -q '^## Instruções de validação$' "$file_path" \
      || fail "$relative_file não possui a seção ## Instruções de validação"
    awk '/^## Jornada da aplicação nesta versão$/{journey=NR} /^## Como usar e validar a aplicação nesta versão$/{usage=NR} /^## Cobertura por comportamento$/{coverage=NR} /^## Instruções de validação$/{validation=NR} END { exit !(journey && usage && coverage && validation && journey < usage && usage < coverage && coverage < validation) }' "$file_path" \
      || fail "$relative_file deve ordenar Jornada, Como usar, Cobertura e Instruções de validação"
    grep -Eiq 'antes|agora|propósito|próxima evolução|ainda falta|limita' "$file_path" \
      || fail "$relative_file não explica a evolução da jornada da aplicação"
    grep -Eiq 'curl|frontend|tela|não há|indisponível|python3|smoke' "$file_path" \
      || fail "$relative_file não explica como usar a aplicação ou declara a integração indisponível"
    grep -Eiq 'unitári|contrato' "$file_path" \
      || fail "$relative_file não registra evidência unitária ou contratual"
    grep -Eiq 'integração|smoke|manual|não se aplica|fora do escopo' "$file_path" \
      || fail "$relative_file não registra validação integrada, smoke/manual ou justificativa de não aplicação"
  fi
done

printf 'handoffs válidos: %s arquivo(s)\n' "${#handoff_files[@]}"
