from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Sheet(Base):
    __tablename__ = 'sheets'

    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    cells: Mapped[List["Cell"]] = relationship(back_populates="sheet")


class Cell(Base):
    __tablename__ = 'cells'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=True)
    sheet_id: Mapped[int] = mapped_column(ForeignKey("sheets.id"), nullable=False)

    # Relationships
    sheet: Mapped["Sheet"] = relationship(back_populates="cells", cascade="all, delete")
