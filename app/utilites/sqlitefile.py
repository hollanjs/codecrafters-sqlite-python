class SQLiteHeaderData:
    __db_file_path__: str
    """
    SQLite header doc - for offset and size
    https://www.sqlite.org/fileformat2.html#the_database_header
    """
    __db_file_header_info__ = {
        "__magic_string__": None,
        "__page_size__": None,
        "__write_version__": None,
        "__read_version__": None,
        "__end_of_page_reserved_space_bytes__": None,
        "__maximum_embedded_payload_fraction__": None,
        "__minimum_embedded_payload_fraction__": None,
        "__leaf_payload_fraction__": None,
        "__file_change_counter__": None,
        "__size_of_db_file_pages__": None,
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

    __db_read_file_byte_buffer__ = None

    def __init__(self, file_path: str):
        # quick check the header for magic string
        self.verify_magic_string(file_path)
        self.db_file_path = file_path
        self.update_db_file_header_data()

    def update_db_file_header_data(self):
        assert self.db_file_path is not None
        with open(self.db_file_path, "rb") as db_bytes:

            self.__db_file_header_info__["__magic_string__"]                      = db_bytes.read(16).decode('ascii')
            self.__db_file_header_info__["__page_size__"]                         = int(db_bytes.read(2).hex(), 16)
            self.__db_file_header_info__["__write_version__"]                     = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__read_version__"]                      = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__end_of_page_reserved_space_bytes__"]  = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__maximum_embedded_payload_fraction__"] = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__minimum_embedded_payload_fraction__"] = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__leaf_payload_fraction__"]             = int(db_bytes.read(1).hex(), 16)
            self.__db_file_header_info__["__file_change_counter__"]               = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__size_of_db_file_pages__"]             = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__first_freelist_trunk_page_num__"]     = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__total_num_freelist_pages__"]          = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__schema_cookie__"]                     = db_bytes.read(4).decode('ascii')
            self.__db_file_header_info__["__schema_format_number__"]              = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__default_page_cache_size__"]           = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__largest_root_btree_page__"]           = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__database_text_encoding__"]            = db_bytes.read(4).decode('ascii')
            self.__db_file_header_info__["__user_version__"]                      = db_bytes.read(4).decode('ascii')
            self.__db_file_header_info__["__incremental_vacuum_mode__"]           = True if db_bytes.read(4).hex() != "00" else False
            self.__db_file_header_info__["__application_id__"]                    = int(db_bytes.read(4).hex(), 16)
            ###########################################################################
            db_bytes.read(20)   ### 20 Bytes Reserved for expansion - just read past it
            ###########################################################################
            self.__db_file_header_info__["__version_valid_for__"]                 = int(db_bytes.read(4).hex(), 16)
            self.__db_file_header_info__["__SQLITE_VERSION_NUMBER__"]             = int(db_bytes.read(4).hex(), 16)

    def show_dbfile_parameters(self):
        import json
        print(json.dumps(self.__db_file_header_info__, indent=4))

    def verify_magic_string(self, file_path):
        MAGIC_STRING = "SQLite format 3\000"
        with open(file_path, "rb") as dbfile:
            assert dbfile.read(16).decode('ascii') == MAGIC_STRING


if __name__ == "__main__":
    sampledb = SQLiteHeaderData("sample.db")
    sampledb.show_dbfile_parameters()