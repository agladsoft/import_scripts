import os
import sys
from arkas import Arkas
from typing import Union, Dict


class Evergreen(Arkas):

    dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    dict_columns_position["goods_tnved"] = None

    def check_errors_in_header(self, row: list, context: dict, no_need_columns: list = None) -> None:
        """
        # ToDo: Writing
        """
        self.check_errors_in_columns([context.get("ship", None), context.get("voyage", None),
                                      context.get("date", None)], context,
                                     "Error code 3: Keys (ship, voyage or date) not in cells", 3)
        self.get_columns_position(row)
        dict_columns_position = self.dict_columns_position.copy()
        for delete_column in no_need_columns:
            del dict_columns_position[delete_column]
        self.check_errors_in_columns(list(dict_columns_position.values()), dict_columns_position,
                                     "Error code 2: Column not in file or changed", 2)

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or (
            not self.is_digit(row[self.dict_columns_position["number_pp"]])
            and row[self.dict_columns_position["container_number"]]
            and row[self.dict_columns_position["goods_name_rus"]])

    def is_duplicate_container_in_row(self, value: str, sign_repeat_container: str, key: str) -> bool:
        """
        # ToDo: Writing
        """
        return value == sign_repeat_container or not value and key == 'city'

    def is_not_duplicate_container_in_row(self, value: str, sign_repeat_container: str) -> bool:
        """
        # ToDo: Writing
        """
        return value not in [sign_repeat_container, '']

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo: Writing
        """
        Arkas.add_frequently_changing_keys(self, row, parsed_record)
        parsed_record['goods_tnved'] = row[self.dict_columns_position["goods_tnved"]] \
            if self.dict_columns_position["goods_tnved"] else None


if __name__ == '__main__':
    parsed_data: Evergreen = Evergreen(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(sign='*'))
