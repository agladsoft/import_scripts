import re
import sys
from __init__ import *
from arkas import Arkas


class CmaCgm(Arkas):

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list, ship_voyage: str = "ship_voyage") -> None:
        """
        Parsing from row the date, ship name and voyage in the cells before the table.
        """
        if re.findall(column, parsing_row):
            if DICT_CONTENT_BEFORE_TABLE[columns] == "date":
                self.parse_date(parsing_row, list_month, context, row)
            elif DICT_CONTENT_BEFORE_TABLE[columns] == "voyage":
                self.parse_ship_and_voyage(parsing_row, row, column, context, "voyage")
            elif DICT_CONTENT_BEFORE_TABLE[columns] == ship_voyage:
                self.parse_ship_and_voyage(parsing_row, row, column, context, "ship")

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        for ship_voyage in row:
            position: int = list(DICT_CONTENT_BEFORE_TABLE.values()).index("ship_voyage_in_other_cells")
            if re.findall(list(DICT_CONTENT_BEFORE_TABLE.keys())[position][0], ship_voyage):
                context[key] = ship_voyage
                break
        self.logger_write.info(f"context now is {context}")


if __name__ == '__main__':
    parsed_data: CmaCgm = CmaCgm(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_reversed=True))
