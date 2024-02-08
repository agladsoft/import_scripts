import sys
from __init__ import *
from arkas import Arkas, telegram


class Safetrance(Arkas):

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Method inheritance from Arkas.
        """
        Arkas.parse_ship_and_voyage(self, parsing_row, row, column, context, key, 0, 2)


if __name__ == '__main__':
    parsed_data: Safetrance = Safetrance(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_reversed=True))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
