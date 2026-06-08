from __future__ import annotations
from typing import TYPE_CHECKING

from .sqliteobservers import SQLiteHeaderObserver

if TYPE_CHECKING:
    from .sqlitefile import SQLiteHeaderData

class SQLiteBTreePageHeader(SQLiteHeaderObserver):
    __btree_bytes__: bytes
    __byte_offset__: int = 0
    page_type: int
    first_free_block: int
    cell_num: int
    cell_content_start: int
    cell_content_num_fragmented_bytes: int

    def has_free_blocks(self):
        self.first_free_block != 0

    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)
        if header_data.__dbfile_header_info__["__magic_string__"] is not None:
            self.__byte_offset__ = 100
        self.__btree_bytes__ = self.__header_data__.__db_header_bytes__[self.__byte_offset__:]
        self.__parse_header__()

    def __parse_header__(self):
        btree_bytes                            = self.__btree_bytes__
        self.page_type                         = int.from_bytes(btree_bytes[:1])
        self.first_free_block                  = int.from_bytes(btree_bytes[1:3])
        self.cell_num                          = int.from_bytes(btree_bytes[3:5])
        self.cell_content_start                = int.from_bytes(btree_bytes[5:7])
        self.cell_content_num_fragmented_bytes = int.from_bytes(btree_bytes[7:8])
    
    def __str__(self):
        import json
        obj_hash = {}
        obj_hash["__byte_offset__"] = self.__byte_offset__
        obj_hash["page_type"] = self.page_type
        obj_hash["first_free_block"] = self.first_free_block
        obj_hash["cell_num"] = self.cell_num
        obj_hash["cell_content_start"] = self.cell_content_start
        obj_hash["cell_content_num_fragmented_bytes"] = self.cell_content_num_fragmented_bytes
        return json.dumps(obj_hash, indent=4)


class SQLiteInteriorIndexBTree(SQLiteBTreePageHeader):
    right_most_pointer: int

    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)

    def __parse_header__(self):
        super().__parse_header__()
        self.right_most_pointer = int.from_bytes(self.__btree_bytes__[8:12])

class SQLiteInteriorTableBTree(SQLiteBTreePageHeader):
    right_most_pointer: int

    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)

    def __parse_header__(self):
        super().__parse_header__()
        self.right_most_pointer = int.from_bytes(self.__btree_bytes__[8:12])

class SQLiteLeafIndexBTree(SQLiteBTreePageHeader):
    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)

class SQLiteLeafTableBTree(SQLiteBTreePageHeader):
    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)


class SQLiteSchemaTable(SQLiteHeaderObserver):
    def __init__(self, header_data: SQLiteHeaderData):
        super().__init__(header_data)
    

def init_btree_header(btree_value: int, header_data: SQLiteHeaderData):
    assert btree_value in [2, 5, 10, 13]
    match btree_value:
        case  2: return SQLiteInteriorIndexBTree(header_data)
        case  5: return SQLiteInteriorTableBTree(header_data)
        case 10: return SQLiteLeafIndexBTree(header_data)
        case 13: return SQLiteLeafTableBTree(header_data)