import sys
from __init__ import *
from typing import Union
from arkas import Arkas, telegram


class Safetrance(Arkas):
    # dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    # dict_columns_position["city"] = None


    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Method inheritance from Arkas.
        """
        Arkas.parse_ship_and_voyage(self, parsing_row, row, column, context, key, 0, 2)

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from Arkas.
        """
        Arkas.add_frequently_changing_keys(self, row, parsed_record)
        parsed_record["city"] = row[self.dict_columns_position["city"]] \
            if self.dict_columns_position["city"] else None




if __name__ == '__main__':
    parsed_data: Safetrance = Safetrance(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_reversed=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
