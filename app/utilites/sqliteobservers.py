from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sqlitefile import SQLiteHeaderData

class SQLiteHeaderObserver:
    __header_data__: SQLiteHeaderData

    def __init__(self, header_data: SQLiteHeaderData):
        self.update_header_data(header_data)
        assert self.__header_data__ is not None
        header_data.register_header_observer(self)

    def update_header_data(self, header_data: SQLiteHeaderData):
        self.__header_data__ = header_data