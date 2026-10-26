import os
import unittest
from unittest.mock import patch

from rastro_ai.observability import observe_operation, update_observation


class ObservabilityTests(unittest.TestCase):
    # /**
    #  * Confirma que o modo padrão não inicializa Langfuse nem faz chamadas externas.
    #  * Histórico: 024-v1 — garante compatibilidade quando a observabilidade está desligada.
    #  */
    def test_disabled_observation_is_a_noop(self) -> None:
        with patch.dict(os.environ, {"LANGFUSE_ENABLED": "false"}, clear=False):
            with observe_operation(
                name="test-operation",
                observation_type="chain",
                input_metadata={"documentId": "doc-1"},
            ) as observation:
                self.assertIsNone(observation)

    # /**
    #  * Confirma que uma falha do processamento continua sendo propagada ao chamador.
    #  * Histórico: 024-v1 — impede que o wrapper de telemetria mascare falhas de indexação.
    #  */
    def test_observation_does_not_swallow_operation_errors(self) -> None:
        with patch.dict(os.environ, {"LANGFUSE_ENABLED": "false"}, clear=False):
            with self.assertRaisesRegex(RuntimeError, "indexing failed"):
                with observe_operation(
                    name="test-operation",
                    observation_type="chain",
                    input_metadata={"documentId": "doc-1"},
                ):
                    raise RuntimeError("indexing failed")

    def test_observation_update_does_not_break_runtime(self) -> None:
        class FailingObservation:
            def update(self, **fields: object) -> None:
                raise RuntimeError("telemetry unavailable")

        update_observation(FailingObservation(), output={"status": "ready"})


if __name__ == "__main__":
    unittest.main()
