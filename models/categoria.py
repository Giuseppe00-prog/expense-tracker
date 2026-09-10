from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class Categoria(Base):
    __tablename__ = "categorie"

    id:Mapped[int] = mapped_column(
        primary_key=True
    )
    nome:Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    def __init__(self, nome:str, id: int | None = None):
        super().__init__()

        if nome is None or not nome.strip():
            raise ValueError("Il nome della categoria non può essere vuoto")

        self.nome = nome

        if id is not None:
            self.id = id