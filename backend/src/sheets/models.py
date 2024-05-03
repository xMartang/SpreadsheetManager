from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from .utils.cell_utils import CELL_TYPE_VALUE_CONVERTER


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

    @property
    def blacklisted_json_columns(self):
        return ["id", "sheet_id"]

    def to_json(self):
        return {
            column_name: self._get_json_value_from_column(column_name) for column_name in self.__table__.columns.keys()
            if column_name not in self.blacklisted_json_columns
        }

    def _get_json_value_from_column(self, column_name):
        if column_name == "value" and self.value is not None:
            return CELL_TYPE_VALUE_CONVERTER[self.type](self.value)

        return getattr(self, column_name)
