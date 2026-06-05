import sys

from dataclasses import dataclass
from app.utilites import sqlitefile as sqlf

# import sqlparse - available if you need it!

database_file_path = sys.argv[1]
command = sys.argv[2]

if command == ".dbinfo":
    sql_file_data = sqlf.SQLiteHeaderData(database_file_path)
    sql_file_data.show_dbfile_parameters()
    with open(database_file_path, "rb") as database_file:
        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)
        # TODO: Uncomment the code below to pass the first stage
        database_file.seek(16)  # Skip the first 16 bytes of the header
        page_size = int.from_bytes(database_file.read(2), byteorder="big")
        print(f"database page size: {page_size}")
else:
    print(f"Invalid command: {command}")
