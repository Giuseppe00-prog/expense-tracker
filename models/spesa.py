from dataclasses import dataclass
from decimal import Decimal

from models.categoria import Categoria
@dataclass
class Spesa:
    """Rappresenta una spesa con descrizione, categoria e importo."""
    descrizione: str
    categoria: Categoria
    importo: Decimal
    id: int | None = None

    def __post_init__(self):
        """Valida i dati della spesa dopo la sua creazione."""

        # Una spesa deve avere un importo non negativo e descrizione valorizzata.
        if self.importo < 0:
            raise ValueError("L'importo non può essere negativo")

        if not self.descrizione.strip():
            raise ValueError("La descrizione non può essere vuota")
