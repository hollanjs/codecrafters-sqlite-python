from struct import unpack_from
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from .sqlitebtree import *


class SQLiteRow:
	def __init__(self):
		pass

# import struct
# struct.unpack('<HHH', b'x\x03\x07\x17\x1b\x1b')

class SQLiteTable():
	betree_header: SQLiteBTreePageHeader
	__header_table_start_byte_offset__: int = 8
	cells: list[int]

	def __init__(self, btree_data: SQLiteBTreePageHeader):
		self.betree_header = btree_data
		if type(self.betree_header) is SQLiteInteriorTableBTree:
			self.__header_table_start_byte_offset__ = 12

		
		

	