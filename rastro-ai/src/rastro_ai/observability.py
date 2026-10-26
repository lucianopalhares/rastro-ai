"""Integração opcional e sanitizada com o Langfuse self-hosted."""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any


def _enabled() -> bool:
    """Indica se o processo possui configuração suficiente para enviar observações."""

    return (
        os.environ.get("LANGFUSE_ENABLED", "false").strip().casefold() == "true"
        and bool(os.environ.get("LANGFUSE_PUBLIC_KEY", "").strip())
        and bool(os.environ.get("LANGFUSE_SECRET_KEY", "").strip())
    )


# /**
#  * Atualiza uma observação sem deixar falhas do coletor afetarem a aplicação.
#  * Existe para manter indexação e geração de embeddings disponíveis mesmo quando o Langfuse está indisponível.
#  * Histórico: 024-v1 — isola atualizações de saída e erro do fluxo principal.
#  */
def update_observation(observation: Any | None, **fields: Any) -> None:
    """Envia campos opcionais ao Langfuse e ignora falhas de telemetria."""

    if observation is None:
        return
    try:
        observation.update(**fields)
    except Exception:
        return


# /**
#  * Abre uma observação Langfuse sem permitir que telemetria interrompa o runtime.
#  * Existe para registrar duração, status e metadados mínimos sem enviar conteúdo documental.
#  * Histórico: 024-v1 — cria o boundary opcional para indexação e embeddings.
#  */
@contextmanager
def observe_operation(
    *,
    name: str,
    observation_type: str,
    input_metadata: dict[str, Any],
) -> Iterator[Any | None]:
    """Produz uma observação ativa quando Langfuse está habilitado e configurado."""

    if not _enabled():
        yield None
        return

    try:
        from langfuse import get_client

        client = get_client()
        observation_context = client.start_as_current_observation(
            as_type=observation_type,
            name=name,
            input=input_metadata,
        )
    except Exception:
        # Falhas de configuração ou de inicialização não alteram o runtime.
        yield None
        return

    with observation_context as observation:
        try:
            yield observation
        except Exception as error:
            update_observation(observation, level="ERROR", status_message=type(error).__name__)
            raise
