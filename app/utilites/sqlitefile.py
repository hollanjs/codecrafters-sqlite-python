from __future__ import annotations
from typing import TYPE_CHECKING

from .sqlitebtree import init_btree_header

if TYPE_CHECKING:
    from .sqlitebtree import SQLiteBTreePageHeader
    from .sqliteobservers import SQLiteHeaderObserver



"""
100 byte header
00000000  53 51 4c 69 74 65 20 66  6f 72 6d 61 74 20 33 00  |SQLite format 3.|
00000010  10 00 01 01 00 40 20 20  00 00 00 05 00 00 00 04  |.....@  ........|
00000020  00 00 00 00 00 00 00 00  00 00 00 02 00 00 00 04  |................|
00000030  00 00 00 00 00 00 00 00  00 00 00 01 00 00 00 00  |................|
00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000050  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 05  |................|
00000060  00 2e 4b 90                                       |..K.            |

8 byte btree
00000060              0d 00 00 00  03|0e c3 00              |    ........    |
                number of cells--->^^|^^^^^<--cell content start   

cell pointer array (number of cells = 3) 
    so we expect 3x 2-byte(big endian) offsets from start of page
    I've seperated them with '|' pipes
00000060                                      [0f 8f|0f 3d| |            ...=|
00000070 |0e c3]                                            |..              |

dead space for future allocations
00000070        00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
...
*
...
first cell start (0ec3)
    notice its the last on in the previous array
    cells are written upwards to save on space(?)
00000ec0           78 03 07 17 1b  1b 01 81 47 74 61 62 6c  |...x.......Gtabl|
00000ed0  65 6f 72 61 6e 67 65 73  6f 72 61 6e 67 65 73 04  |eorangesoranges.|
00000ee0  43 52 45 41 54 45 20 54  41 42 4c 45 20 6f 72 61  |CREATE TABLE ora|
00000ef0  6e 67 65 73 0a 28 0a 09  69 64 20 69 6e 74 65 67  |nges.(..id integ|
00000f00  65 72 20 70 72 69 6d 61  72 79 20 6b 65 79 20 61  |er primary key a|
00000f10  75 74 6f 69 6e 63 72 65  6d 65 6e 74 2c 0a 09 6e  |utoincrement,..n|
00000f20  61 6d 65 20 74 65 78 74  2c 0a 09 64 65 73 63 72  |ame text,..descr|
00000f30  69 70 74 69 6f 6e 20 74  65 78 74 0a 29           |iption text.)   |

second cell start (0f3d)
00000f30                                          50 02 06  |             P..|
00000f40  17 2b 2b 01 59 74 61 62  6c 65 73 71 6c 69 74 65  |.++.Ytablesqlite|
00000f50  5f 73 65 71 75 65 6e 63  65 73 71 6c 69 74 65 5f  |_sequencesqlite_|
00000f60  73 65 71 75 65 6e 63 65  03 43 52 45 41 54 45 20  |sequence.CREATE |
00000f70  54 41 42 4c 45 20 73 71  6c 69 74 65 5f 73 65 71  |TABLE sqlite_seq|
00000f80  75 65 6e 63 65 28 6e 61  6d 65 2c 73 65 71 29     |uence(name,seq) |

start of third cell (0f8f)
00000f80                                                6f  |               o|
00000f90  01 07 17 19 19 01 81 39  74 61 62 6c 65 61 70 70  |.......9tableapp|
00000fa0  6c 65 73 61 70 70 6c 65  73 02 43 52 45 41 54 45  |lesapples.CREATE|
00000fb0  20 54 41 42 4c 45 20 61  70 70 6c 65 73 0a 28 0a  | TABLE apples.(.|
00000fc0  09 69 64 20 69 6e 74 65  67 65 72 20 70 72 69 6d  |.id integer prim|
00000fd0  61 72 79 20 6b 65 79 20  61 75 74 6f 69 6e 63 72  |ary key autoincr|
00000fe0  65 6d 65 6e 74 2c 0a 09  6e 61 6d 65 20 74 65 78  |ement,..name tex|
00000ff0  74 2c 0a 09 63 6f 6c 6f  72 20 74 65 78 74 0a 29  |t,..color text.)|

IDK what this is yet...
00001000  0d 00 00 00 04 0f a1 00  0f e3 0f d6 0f bd 0f a1  |................|
00001010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
"""





class SQLiteFileHeaderData:
    __HEADER_BYTE_LENGTH__: int = 100

    __dbfile_path__: str
    __db_file_bytes__: bytes

    __observers__: list[SQLiteHeaderObserver] = []

    __schema_table_btree__: SQLiteBTreePageHeader

    """
    SQLite header doc - for offset and size
    https://www.sqlite.org/fileformat2.html#the_database_header
    """
    __dbfile_header_info__ = {
        "__magic_string__": None,
        "__page_size__": None,
        "__write_version__": None,
        "__read_version__": None,
        "__end_of_page_reserved_space_bytes__": None,
        "__maximum_embedded_payload_fraction__": None,
        "__minimum_embedded_payload_fraction__": None,
        "__leaf_payload_fraction__": None,
        "__file_change_counter__": None,
        "__size_of_dbfile_pages__": None,
        "__first_freelist_trunk_page_num__": None,
        "__total_num_freelist_pages__": None,
        "__schema_cookie__": None,
        "__schema_format_number__": None,
        "__default_page_cache_size__": None,
        "__largest_root_btree_page__": None,
        "__database_text_encoding__": None,
        "__user_version__": None,
        "__incremental_vacuum_mode__": None,
        "__application_id__": None,
        "__version_valid_for__": None,
        "__SQLITE_VERSION_NUMBER__": None
    }

    def __update_observers__(self):
        for observer in self.__observers__:
            observer.update_header_data(self)

    def register_header_observer(self, observer: SQLiteHeaderObserver):
        self.__observers__.append(observer)

    def unregister_header_observer(self, observer: SQLiteHeaderObserver):
        self.__observers__.remove(observer)
        
    def __init__(self, file_path: str):
        # quick check the header for magic string
        self.verify_magic_string(file_path)
        self.dbfile_path = file_path
        self.update_header_properties()

    def update_header_properties(self):
        self.__update_dbfile_header_bytes__()
        self.__update_dbfile_header_data__()
        self.__update_observers__()

    def __update_dbfile_header_bytes__(self):
        assert self.dbfile_path is not None
        with open(self.dbfile_path, "rb") as db_bytes:
            self.__db_file_bytes__ = db_bytes.read()

    def __update_dbfile_header_data__(self):
        assert self.__db_file_bytes__ is not None

        # save some horizontal space
        header  = self.__dbfile_header_info__
        h_bytes = self.__db_file_bytes__

        header["__magic_string__"]                      = h_bytes[:16].decode()      #db_bytes.read(16).decode('ascii')
        header["__page_size__"]                         = int.from_bytes(h_bytes[16:18])      #int(db_bytes.read(2).hex(), 16)
        header["__write_version__"]                     = int.from_bytes(h_bytes[18:19])      #int(db_bytes.read(1).hex(), 16)
        header["__read_version__"]                      = int.from_bytes(h_bytes[19:20])      #int(db_bytes.read(1).hex(), 16)
        header["__end_of_page_reserved_space_bytes__"]  = int.from_bytes(h_bytes[20:21])      #int(db_bytes.read(1).hex(), 16)
        header["__maximum_embedded_payload_fraction__"] = int.from_bytes(h_bytes[21:22])      #int(db_bytes.read(1).hex(), 16)
        header["__minimum_embedded_payload_fraction__"] = int.from_bytes(h_bytes[22:23])      #int(db_bytes.read(1).hex(), 16)
        header["__leaf_payload_fraction__"]             = int.from_bytes(h_bytes[23:24])      #int(db_bytes.read(1).hex(), 16)
        header["__file_change_counter__"]               = int.from_bytes(h_bytes[24:28])      #int(db_bytes.read(4).hex(), 16)
        header["__size_of_dbfile_pages__"]             = int.from_bytes(h_bytes[28:32])      #int(db_bytes.read(4).hex(), 16)
        header["__first_freelist_trunk_page_num__"]     = int.from_bytes(h_bytes[32:36])      #int(db_bytes.read(4).hex(), 16)
        header["__total_num_freelist_pages__"]          = int.from_bytes(h_bytes[36:40])      #int(db_bytes.read(4).hex(), 16)
        header["__schema_cookie__"]                     = h_bytes[40:44].decode()      #db_bytes.read(4).decode('ascii')
        header["__schema_format_number__"]              = int.from_bytes(h_bytes[44:48])      #int(db_bytes.read(4).hex(), 16)
        header["__default_page_cache_size__"]           = int.from_bytes(h_bytes[48:52])      #int(db_bytes.read(4).hex(), 16)
        header["__largest_root_btree_page__"]           = int.from_bytes(h_bytes[52:56])      #int(db_bytes.read(4).hex(), 16)
        header["__database_text_encoding__"]            = h_bytes[56:60].decode()      #db_bytes.read(4).decode('ascii')
        header["__user_version__"]                      = h_bytes[60:64].decode()      #db_bytes.read(4).decode('ascii')
        header["__incremental_vacuum_mode__"]           = True if int.from_bytes(h_bytes[64:68]) != 0 else False      #True if db_bytes.read(4).hex() != "00" else False
        header["__application_id__"]                    = int.from_bytes(h_bytes[68:72])      #int(db_bytes.read(4).hex(), 16)
        ###########################################################################
        ###             20 Bytes Reserved for expansion - just skip             ### [ 72 : 92 ]
        ###########################################################################
        header["__version_valid_for__"]                 = int.from_bytes(h_bytes[92:96])      #int(db_bytes.read(4).hex(), 16)
        header["__SQLITE_VERSION_NUMBER__"]             = int.from_bytes(h_bytes[96:100])      #int(db_bytes.read(4).hex(), 16)

        self.__schema_table_btree__ = init_btree_header(int.from_bytes(h_bytes[100:101]), self)

    def __str__(self):
        import json
        return json.dumps(self.__dbfile_header_info__, indent=4)

    def verify_magic_string(self, file_path):
        MAGIC_STRING = "SQLite format 3\000"
        with open(file_path, "rb") as dbfile:
            assert dbfile.read(16).decode('ascii') == MAGIC_STRING




if __name__ == "__main__":
    sampledb = SQLiteFileHeaderData("sample.db")
    print(f"database page size: {sampledb.__dbfile_header_info__["__page_size__"]}")
    print(f"Sample.db has {sampledb.__schema_table_btree__.cell_num} tables")

