# class TableBTree


class SQLiteHeaderData:
    __dbfile_path__: str
    __db_header_bytes__: bytes

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


    def __init__(self, file_path: str):
        # quick check the header for magic string
        self.verify_magic_string(file_path)
        self.dbfile_path = file_path
        self.update_header_properties()

    def update_header_properties(self):
        self.__update_dbfile_header_bytes__()
        self.__update_dbfile_header_data__()

    def __update_dbfile_header_bytes__(self):
        assert self.dbfile_path is not None
        with open(self.dbfile_path, "rb") as db_bytes:
            self.__db_header_bytes__ = db_bytes.read()

    def __update_dbfile_header_data__(self):
        assert self.__db_header_bytes__ is not None

        # save some horizontal space
        header  = self.__dbfile_header_info__
        h_bytes = self.__db_header_bytes__

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

    def show_dbfile_parameters(self):
        import json
        print(json.dumps(self.__dbfile_header_info__, indent=4))

    def verify_magic_string(self, file_path):
        MAGIC_STRING = "SQLite format 3\000"
        with open(file_path, "rb") as dbfile:
            assert dbfile.read(16).decode('ascii') == MAGIC_STRING


if __name__ == "__main__":
    sampledb = SQLiteHeaderData("sample.db")
    sampledb.show_dbfile_parameters()