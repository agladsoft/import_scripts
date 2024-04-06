import os
import sys
from arkas import Arkas, telegram
from typing import Union, Dict


class Evergreen(Arkas):

    dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    dict_columns_position["tnved"] = None

    def check_errors_in_header(self, row: list, context: dict, no_need_columns: list = None) -> None:
        """
        Checking for columns in the entire document, counting more than just columns on the same line.
        """
        if no_need_columns is None:
            no_need_columns = []
        self.check_errors_in_columns([context.get("ship_name", None), context.get("voyage", None),
                                      context.get("shipment_date", None)], context,
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
            and row[self.dict_columns_position["goods_name"]])

    def is_duplicate_container_in_row(self, value: str, sign_repeat_container: str, key: str) -> bool:
        """
        Getting a boolean value to confirm that this column needs to be replaced with
        the value of the column of the previous row.
        """
        return value == sign_repeat_container or not value and key == 'city'

    def is_not_duplicate_container_in_row(self, value: str, sign_repeat_container: str) -> bool:
        """
        Getting a boolean value to confirm that this column does not need to be replaced with
        the value of the column of the previous row.
        """
        return value not in [sign_repeat_container, '']

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from Arkas.
        """
        Arkas.add_frequently_changing_keys(self, row, parsed_record)
        parsed_record["tnved"] = row[self.dict_columns_position["tnved"]] \
            if self.dict_columns_position["tnved"] else None


if __name__ == '__main__':
    parsed_data: Evergreen = Evergreen(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(sign='*'))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
