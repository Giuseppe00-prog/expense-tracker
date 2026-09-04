from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Spesa:
    """Rappresenta una spesa con descrizione, categoria e importo."""
    descrizione: str
    categoria: str
    importo: Decimal
    id: int | None = None

    def __post_init__(self):
        """Valida i dati della spesa dopo la sua creazione."""

        # Una spesa deve avere un importo non negativo e descrizione e categoria valorizzate.
        if self.importo < 0 or not self.descrizione.strip() or not self.categoria.strip():
            raise ValueError("Inserire valori validi")
