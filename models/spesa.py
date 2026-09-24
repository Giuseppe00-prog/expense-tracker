from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from models.categoria import Categoria
from datetime import date

class Spesa(Base):
    """Rappresenta una spesa con descrizione, categoria e importo."""
    __tablename__ = "spese"

    id:Mapped[int]=mapped_column(primary_key=True)
    descrizione:Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    importo:Mapped[Decimal]=mapped_column(
        Numeric(10,2),
        nullable=False
    )
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorie.id"),
        nullable=False
    )
    data: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    categoria:Mapped[Categoria]= relationship()

    def __init__(
            self,
            descrizione: str,
            categoria: Categoria,
            importo: Decimal,
            data: date,
            id: int | None = None
    ):
        """Valida i dati della spesa dopo la sua creazione."""
        super().__init__()

        # Una spesa deve avere un importo non negativo e descrizione valorizzata.
        if importo < 0:
            raise ValueError("L'importo non può essere negativo")

        if not descrizione.strip():
            raise ValueError("La descrizione non può essere vuota")

        self.descrizione = descrizione
        self.importo = importo
        self.categoria = categoria
        self.data = data

        if id is not None:
            self.id = id
