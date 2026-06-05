


class parsedSQLiteFile:
    db_file_path: str
    file_hex_data: str

    # offset and size are in bytes
    __magic_string__: str                       #OFFSET:  0; SIZE: 16 :: must equal "SQLite format 3\000" to be a valid file
    __page_size__: int                          #OFFSET: 16; SIZE:  2 :: Must be a power of two between 512 and 32768 inclusive, or the value 1 representing a page size of 65536.
    __write_version__: int                      #OFFSET: 18; SIZE:  1 :: 1 for legacy; 2 for WAL.
    __read_version__: int                       #OFFSET: 19; SIZE:  1 :: 1 for legacy; 2 for WAL.
    __end_of_page_reserved_space_bytes__: int   #OFFSET: 20; SIZE:  1 :: usually 0
    __maximum_embedded_payload_fraction__: int  #OFFSET: 21; SIZE:  1 :: must be 64
    __minimum_embedded_payload_fraction__: int  #OFFSET: 22; SIZE:  1 :: must be 32
    __leaf_payload_fraction__: int
    __file_change_counter__: int
    __size_of_db_file_pages__: int
    __first_freelist_trunk_page_num__: int
    __total_num_freelist_pages__: int
    __schema_cookie__: str
    __schema_format_number__: int
    __default_page_cache_size__: int


















fff    

    def __init__(self, file_path: str):
        # quick check the header for magic string
        self.verify_magic_string(file_path)

        self.db_file_path = file_path
        with open(self.db_file_path, "rb") as dbfile:
            self.file_hex_data = dbfile.read().hex()


    def verify_magic_string(self, file_path):
        MAGIC_STRING = "SQLite format 3\000"
        with open(file_path, "rb") as dbfile:
            assert dbfile.read(16).decode('ascii') == MAGIC_STRING

    def hex_to_int(self, hex_string):
        return int(hex_string, 16)