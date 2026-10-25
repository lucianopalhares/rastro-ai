from pathlib import Path
import os
import subprocess
import sys
import unittest


ROOT = Path(__file__).parents[1]
SRC = ROOT / "src"


# /**
#  * Confirma que o runtime não inicia sem o backend persistente de embeddings.
#  * Existe para impedir regressão para busca lexical silenciosa.
#  * Histórico: v1 — cobre ausência e seleção explícita do backend.
#  */
class RuntimeVectorStoreTests(unittest.TestCase):
    """Verifica que o runtime não degrada para o store lexical em memória."""

    # /** Histórico: v1 — rejeita configuração ausente do backend persistente. */
    def test_runtime_rejects_missing_backend_configuration(self) -> None:
        environment = os.environ.copy()
        environment.pop("VECTOR_STORE_BACKEND", None)
        environment["PYTHONPATH"] = str(SRC)

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import rastro_ai.retrieval",
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("VECTOR_STORE_BACKEND must be 'postgres'", result.stderr)

    # /** Histórico: v1 — rejeita configuração lexical no runtime. */
    def test_runtime_rejects_lexical_backend_configuration(self) -> None:
        environment = os.environ.copy()
        environment["VECTOR_STORE_BACKEND"] = "memory"
        environment["PYTHONPATH"] = str(SRC)

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import rastro_ai.retrieval",
            ],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("VECTOR_STORE_BACKEND must be 'postgres'", result.stderr)


if __name__ == "__main__":
    unittest.main()
