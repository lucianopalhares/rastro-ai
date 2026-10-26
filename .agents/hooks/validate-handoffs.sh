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

STATE_CONTRACT_FILE="$ROOT_DIR/docs/handoff-contracts/02-modelo-estado-decisao-e-evidencia.md"
[[ -f "$STATE_CONTRACT_FILE" ]] || fail "o contrato de estado, decisão e evidência não foi encontrado"
grep -q '^## Camada 1 — Estado$' "$STATE_CONTRACT_FILE" || fail "o contrato não possui a camada de estado"
grep -q '^## Camada 2 — Decisão$' "$STATE_CONTRACT_FILE" || fail "o contrato não possui a camada de decisão"
grep -q '^## Camada 3 — Evidência$' "$STATE_CONTRACT_FILE" || fail "o contrato não possui a camada de evidência"

CURRENT_FILE="$ROOT_DIR/handoffs/CURRENT.md"
SEQUENCE_FILE="$ROOT_DIR/handoffs/SEQUENCE.md"
[[ -f "$CURRENT_FILE" ]] || fail "handoffs/CURRENT.md não foi encontrado"
[[ -f "$SEQUENCE_FILE" ]] || fail "handoffs/SEQUENCE.md não foi encontrado"

current_value="$(tr -d '[:space:]' < "$CURRENT_FILE")"
if [[ "$current_value" != "idle" ]]; then
  [[ "$current_value" =~ ^[0-9]{3}$ ]] || fail "CURRENT.md deve conter um número de três dígitos ou idle"
  active_task_line="$(grep -E "^- Implementação ativa: .*\`${current_value}-" "$SEQUENCE_FILE" || true)"
  [[ -n "$active_task_line" ]] || fail "CURRENT.md aponta para $current_value, mas SEQUENCE.md não declara essa implementação como ativa"
  task_readme="$(find "$ROOT_DIR/handoffs" -maxdepth 2 -type f -path "*/${current_value}-*/README.md" -print -quit)"
  [[ -n "$task_readme" ]] || fail "CURRENT.md aponta para $current_value, mas o README da implementação não existe"
  task_status="$(grep -m1 -oE 'Status: `[^`]+`' "$task_readme" | sed -E 's/.*`([^`]+)`.*/\1/' || true)"
  case "$task_status" in
    proposed|approved|applied) ;;
    *) fail "CURRENT.md aponta para $current_value, mas a tarefa está com status final ou ausente: ${task_status:-desconhecido}" ;;
  esac
fi

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
