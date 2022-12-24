import re
import os
import sys
from admiral import Admiral
from typing import Union, Dict
from evergreen import Evergreen


class Msc(Evergreen):

    dict_columns_position: Dict[str, Union[None, int]] = Evergreen.dict_columns_position
    del dict_columns_position["container_size"]
    del dict_columns_position["container_type"]
    dict_columns_position["container_size_and_type"] = None

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        Admiral.parse_ship_and_voyage(self, parsing_row, row, column, context, key)

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list, ship_voyage: str = "ship_voyage") -> None:
        Admiral.parse_content_before_table(self, column, columns, parsing_row, list_month, context, row,
                                           "ship_voyage_msc")

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        container_number = re.sub(r'(?<=\w) (?=\d)', '', row[self.dict_columns_position["container_number"]].strip())
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or (
            not self.is_digit(row[self.dict_columns_position["number_pp"]])
            and bool(re.findall(r"\w{4}\d{7}", container_number))
            and row[self.dict_columns_position["container_size_and_type"]])

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        parsed_record['container_size'] = \
            int(re.findall(r"\d{2}", row[self.dict_columns_position["container_size_and_type"]].strip())[0])
        parsed_record['container_type'] = \
            re.findall("[A-Z a-z]{1,4}", row[self.dict_columns_position["container_size_and_type"]].strip())[0]
        city: list = list(row[self.dict_columns_position["consignee"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()
        parsed_record['goods_tnved'] = row[self.dict_columns_position["goods_tnved"]] \
            if self.dict_columns_position["goods_tnved"] else None


if __name__ == '__main__':
    parsed_data = Msc(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
