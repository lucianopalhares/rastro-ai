"""Adaptador de arquivos UTF-8 para o caso de uso de indexação."""

from pathlib import Path

from ...domain.services import normalize_text


SUPPORTED_EXTENSIONS = {".md", ".txt"}


class Utf8FileTextExtractor:
    """Lê arquivos locais `.md` e `.txt` e entrega texto normalizado ao domínio."""

    def extract(self, path: str | Path) -> str:
        """Valida a extensão, lê UTF-8 e rejeita documentos sem conteúdo."""

        file_path = Path(path)
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
            raise ValueError(f"Only {supported} files are supported")

        text = normalize_text(file_path.read_text(encoding="utf-8"))
        if not text:
            raise ValueError("Document text is required")
        return text
