"""Isolamento de resultados por projeto."""

from collections.abc import Iterable


# /**
#  * Responde: “a busca trouxe somente informações do projeto consultado?”.
#  * Um resultado 1 significa que nenhum chunk de outro projeto vazou; 0 significa que houve
#  * pelo menos um resultado pertencente a outro projeto. É uma proteção de segurança, não de relevância.
#  * Exemplo: consulta do projeto A retornando apenas A resulta em 1; qualquer chunk de B leva a 0.
#  * Ordem: etapa 4.1, logo depois de receber os resultados e antes das métricas de ranking.
#  * Histórico: 026-v2 — extrai isolamento; 026-v4 — documenta a ordem; 027-v4 — simplifica a explicação.
#  */
def project_isolation(result_project_ids: Iterable[str], requested_project_id: str) -> float:
    """Retorna um quando nenhum resultado pertence a outro projeto, senão zero."""

    return float(all(project_id == requested_project_id for project_id in result_project_ids))
