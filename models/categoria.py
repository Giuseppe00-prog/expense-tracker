from dataclasses import dataclass

@dataclass
class Categoria:
    nome: str
    id: int | None = None

    def __post_init__(self):
        if not self.nome.strip():
            raise ValueError("Il nome della categoria non può essere vuoto")