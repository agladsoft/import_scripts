import re
import sys
from __init__ import *
from arkas import Arkas
from admiral import Admiral, telegram


class United(Admiral):
    dict_columns_position: Dict[str, Union[None, int]] = Admiral.dict_columns_position
    del dict_columns_position["container_size"]

    @staticmethod
    def remove_keys_in_data(word: str) -> str:
        """
        Removing keys in voyage, ship and date.
        """
        return Arkas.remove_keys_in_data(word)

    def parse_date_format_russia(self, parsing_row, context):
        """
        Getting the date in "%d.%m-%y" format.
        """
        Arkas.parse_date_format_russia(self, parsing_row, context)

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        try:
            Admiral.parse_date(self, parsing_row, month_list, context, row)
        except IndexError:
            Arkas.parse_date(self, parsing_row, month_list, context, row)

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        ship_and_voyage_list: list = parsing_row.replace(column, "").replace("_", " ").strip().rsplit(' ', 1)
        context["ship_name"] = ship_and_voyage_list[0].strip()
        context["voyage"] = re.sub(r'[^\w\s]', '', ship_and_voyage_list[1])
        self.logger_write.info(f"context now is {context}")


if __name__ == '__main__':
    parsed_data: United = United(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
