import itertools
import os
import sys
import re
from __init__ import *
from arkas import Arkas, telegram


class Safetrance(Arkas):

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 2) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        index: int = 0
        for ship_voyage in row:
            position: int = list(DICT_CONTENT_BEFORE_TABLE.values()).index("ship_voyage_in_other_cells")
            if re.findall(list(DICT_CONTENT_BEFORE_TABLE.keys())[position][0], ship_voyage):
                if index == index_ship:
                    context["ship_name"] = self.remove_keys_in_data(ship_voyage)
                elif index == index_voyage:
                    context['voyage'] = self.remove_keys_in_data(ship_voyage)
                index += 1
        self.logger_write.info(f"context now is {context}")


if __name__ == '__main__':
    parsed_data: Safetrance = Safetrance(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_reversed=True))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
