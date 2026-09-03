from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Spesa:
    descrizione: str
    categoria: str
    importo: Decimal

    def __post_init__(self):
        if self.importo < 0 or not self.descrizione.strip() or not self.categoria.strip():
            raise ValueError("Inserire valori validi")
