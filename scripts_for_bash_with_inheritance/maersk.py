import sys
from __init__ import *
from cma_cgm import CmaCgm
from admiral import Admiral
from arkas import Arkas
from datetime import datetime


class Maersk(CmaCgm):

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        Arkas.parse_ship_and_voyage(self, parsing_row, row, column, context, key, 1, 2)

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%d-%B-%Y" format.
        """
        self.logger_write.info(u"Checking if we are on common line with number...")
        date = datetime.strptime(parsing_row.rsplit(' ')[0], "%d-%B-%Y")
        context['date'] = str(date.date())
        self.logger_write.info(f"context now is {context}")

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list) -> None:
        Admiral.parse_content_before_table(self, column, columns, parsing_row, list_month, context, row)


if __name__ == '__main__':
    parsed_data = Maersk(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(coefficient_of_header=55))
