import sys

from dataclasses import dataclass
from app.utilites.sqlitefile import SQLiteHeaderData


# import sqlparse - available if you need it!

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    # sql_file_data = sqlf.SQLiteHeaderData(database_file_path)
    # sql_file_data.show_dbfile_parameters()
    # with open(database_file_path, "rb") as database_file:
    sampledb = SQLiteHeaderData(database_file_path)
    print(f"database page size: {sampledb.__dbfile_header_info__["__page_size__"]}")
    print(f"number of tables: {sampledb.__schema_table__.cell_num}")
else:
    print(f"Invalid command: {command}")
