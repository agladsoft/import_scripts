import sys
from __init__ import *
from typing import Union
from admiral import Admiral
from economou import Economou


class Fesco(Economou):

    dict_columns_position: Dict[str, Union[bool, int]] = Admiral.dict_columns_position

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        # ToDo:
        """
        Economou.parse_ship_and_voyage(self, parsing_row, row, column, context, key)

    def is_table_starting(self, row: list) -> bool:
        """
        # ToDo:
        """
        return Admiral.is_table_starting(self, row)

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        Admiral.add_frequently_changing_keys(self, row, parsed_record)


if __name__ == '__main__':
    parsed_data: Fesco = Fesco(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
