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


if __name__ == '__main__':
    parsed_data: United = United(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
