from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Sheet(Base):
    __tablename__ = 'sheets'

    id: Mapped[int] = mapped_column(primary_key=True)

    # Relationships
    columns: Mapped[List["Column"]] = relationship(back_populates="sheet")


class Column(Base):
    __tablename__ = 'columns'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    sheet_id: Mapped[int] = mapped_column(ForeignKey("sheets.id"), nullable=False)

    # Relationships
    sheet: Mapped["Sheet"] = relationship(back_populates="columns", cascade="all, delete")
    cells: Mapped[List["Cell"]] = relationship(back_populates="column")

    @property
    def blacklisted_json_columns(self):
        return ["id", "sheet_id"]


class Cell(Base):
    __tablename__ = 'cells'

    id: Mapped[int] = mapped_column(primary_key=True)
    row_index: Mapped[int] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    column_id: Mapped[int] = mapped_column(ForeignKey("columns.id"), nullable=False)

    # Relationships
    column: Mapped["Column"] = relationship(back_populates="cells", cascade="all, delete")

    @property
    def blacklisted_json_columns(self):
        return ["id", "column_id"]
