import sys
from __init__ import *
from arkas import Arkas
from typing import Union
from admiral import Admiral
from evergreen import Evergreen
from datetime import datetime


class Maersk(Evergreen):

    dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    del dict_columns_position["number_pp"]
    del dict_columns_position["container_size"]
    del dict_columns_position["container_type"]
    del dict_columns_position["container_seal"]
    del dict_columns_position["shipper_country"]
    del dict_columns_position["goods_tnved"]
    dict_columns_position["container_size_and_type"] = None

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

    def check_errors_in_header(self, row: list, context: dict, no_need_column: str = "goods_tnved") -> None:
        Evergreen.check_errors_in_header(self, row, context, "goods_name_rus")

    def is_table_starting(self, row: list) -> tuple:
        """
        Understanding when a headerless table starts.
        """
        return bool(row[self.dict_columns_position["consignment"]]), \
            bool(row[self.dict_columns_position["shipper"]]), \
            bool(row[self.dict_columns_position["consignee"]]), \
            bool(row[self.dict_columns_position["container_number"]]), \
            bool(row[self.dict_columns_position["container_size_and_type"]]), \
            bool(row[self.dict_columns_position["goods_weight"]])


if __name__ == '__main__':
    parsed_data = Maersk(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
