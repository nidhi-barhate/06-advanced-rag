from pathlib import Path
from pypdf import PdfReader

class DocumentLoaderService:
    def load(
            self,
            path: Path
    ) -> str:
        suffix = path.suffix.lower()
        if suffix == ".txt":
            return self._load_txt(path)
        if suffix == ".pdf":
            return self._load_pdf(path)
        raise ValueError(
            f"Unsupported file type: {suffix}"
        )

    def _load_txt(
            self,
            path: Path
    ) -> str:
        return path.read_text(
            encoding="utf-8"
        )

    def _load_pdf(
            self,
            path: Path
    ) -> str:
        reader = PdfReader(path)
        text = []
        for page in reader.pages:
            text.append(
                page.extract_text()
            )
        return "\n".join(text)