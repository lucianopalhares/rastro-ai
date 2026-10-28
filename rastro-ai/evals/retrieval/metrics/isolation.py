"""Isolamento de resultados por projeto."""

from collections.abc import Iterable


# /**
#  * Verifica se todos os resultados pertencem ao projeto consultado.
#  * Existe para transformar vazamento entre tenants em uma métrica explícita de segurança.
#  * Ordem: etapa 4.1, imediatamente após normalizar os resultados e antes do ranking.
#  * Histórico: 026-v2 — extrai isolamento; 026-v4 — documenta a ordem.
#  */
def project_isolation(result_project_ids: Iterable[str], requested_project_id: str) -> float:
    """Retorna um quando nenhum resultado pertence a outro projeto, senão zero."""

    return float(all(project_id == requested_project_id for project_id in result_project_ids))
