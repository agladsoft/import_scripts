import re
import sys
from __init__ import *
from arkas import Arkas


class Economou(Arkas):

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str):
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        index: int = 0
        for ship_voyage in row:
            position: int = list(DICT_CONTENT_BEFORE_TABLE.values()).index("ship_voyage_in_other_cells")
            if re.findall(list(DICT_CONTENT_BEFORE_TABLE.keys())[position][0], ship_voyage):
                if index == 0:
                    context['ship'] = ship_voyage.strip()
                elif index == 1:
                    context['voyage'] = ship_voyage.strip()
                index += 1
        self.logger_write.info(f"context now is {context}")


if __name__ == '__main__':
    parsed_data = Economou(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
