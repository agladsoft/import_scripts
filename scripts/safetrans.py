import sys
from __init__ import *
from typing import Union
from admiral import Admiral
from arkas import Arkas, telegram


class Safetrance(Arkas, Admiral):
    dict_columns_position: Dict[str, Union[None, int]] = Admiral.dict_columns_position
    del dict_columns_position["container_size"]
    del dict_columns_position["container_type"]

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Method inheritance from Arkas.
        """
        if len([i for i in row if i]) == 1:
            Admiral.parse_ship_and_voyage(self, parsing_row, row, column, context, key)
        else:
            Arkas.parse_ship_and_voyage(self, parsing_row, row, column, context, key, 0, 2)

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from Arkas.
        """
        try:
            Arkas.add_frequently_changing_keys(self, row, parsed_record)
            parsed_record["city"] = row[self.dict_columns_position["city"]] \
                if self.dict_columns_position["city"] else None
        except KeyError:
            Admiral.add_frequently_changing_keys(self, row, parsed_record)

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        try:
            Arkas.parse_date(self, parsing_row, month_list, context, row)
        except ValueError:
            Admiral.parse_date(self, parsing_row, month_list, context, row)


if __name__ == '__main__':
    parsed_data: Safetrance = Safetrance(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_reversed=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
