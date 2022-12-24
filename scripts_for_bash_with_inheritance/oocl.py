import re
import sys
from msc import Msc
from __init__ import *
from arkas import Arkas
from typing import Union, Dict


class Oocl(Msc):

    dict_columns_position: Dict[str, Union[None, int]] = Msc.dict_columns_position
    del dict_columns_position["container_size_and_type"]
    dict_columns_position["container_size"] = None
    dict_columns_position["container_type"] = None

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        Arkas.add_frequently_changing_keys(self, row, parsed_record)

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list, ship_voyage: str = "ship_voyage") -> None:
        """
        Parsing from row the date, ship name and voyage in the cells before the table.
        """
        if re.findall(column, parsing_row):
            if DICT_CONTENT_BEFORE_TABLE[columns] == "date":
                self.parse_date(parsing_row, list_month, context, row)
            elif DICT_CONTENT_BEFORE_TABLE[columns] == ship_voyage:
                self.parse_ship_and_voyage2(row, context)


if __name__ == '__main__':
    parsed_data: Oocl = Oocl(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
