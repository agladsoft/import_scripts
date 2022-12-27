import os
import sys
from typing import Tuple
from admiral import Admiral


class Verim(Admiral):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]].replace('/', '.')) \
            or row[self.dict_columns_position["goods_name_rus"]]

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from Admiral.
        """
        Admiral.add_frequently_changing_keys(self, row, parsed_record)
        parsed_record['container_seal'] = row[self.dict_columns_position["container_seal"]].strip()

    @staticmethod
    def update_values_duplicate_containers(set_index: set, index: int, list_data: list, is_reversed: bool,
                                           sign_repeat_container: str) -> None:
        """
        Update values if the given column is duplicate from the previous row.
        """
        key_list: list = list(list_data[list(set_index)[0]].keys())
        val_list: list = list(list_data[list(set_index)[0]].values())
        positions: list = [i for i, d in enumerate(val_list) if d == sign_repeat_container]
        for index_container in list(set_index):
            for position in positions:
                list_data[index_container][key_list[position]] = list_data[index][key_list[position]] \
                    if is_reversed else list_data[index - len(set_index) - 1][key_list[position]]
            set_index.pop()

    @staticmethod
    def find_duplicate_containers(is_duplicate_containers_in_line: bool, is_reversed: bool, *args: any) \
            -> Tuple[bool, bool]:
        """
        Find columns that are duplicate from previous row.
        """
        for key, value in zip(args[1], args[2]):
            if value == args[3]:
                try:
                    args[6].add(args[8])
                    is_duplicate_containers_in_line: bool = True
                    if args[0]["container_seal"] == list(args[9].values())[-1] and list(args[9].keys())[-1] != '':
                        is_reversed: bool = False
                    args[5][key] = args[7][key]
                except (KeyError, IndexError):
                    continue
            else:
                args[4][key] = value
            if value != args[3]:
                args[7][key] = value
        return is_duplicate_containers_in_line, is_reversed

    def is_empty_values_in_keys(self, row: dict, index: int) -> None:
        """
        If the data for these fields is empty, then we will not be able to determine where the containers are repeated.
        """
        if row["container_number"] == '' and row["container_seal"] == '' and row['container_type'] == '' \
                and row['container_size'] == '':
            self.logger_write.error(f'Container_seal is empty on row {index}')
            print(f"5_in_row_{index + 1}", file=sys.stderr)
            sys.exit(5)

    def fill_data_with_duplicate_containers(self, list_data: list, sign_repeat_container: str,
                                            is_reversed: bool) -> list:
        """
        Filling empty cells with data in repeating containers.
        """
        context: dict = {}
        dict_last_value: dict = {}
        set_index: set = set()
        last_container_seal_and_container_dict: dict = {}
        for index, row in enumerate(list_data):
            self.is_empty_values_in_keys(row, index)
            is_duplicate_containers_in_line: bool = False
            keys_list: list = list(row.keys())
            values_list: list = list(row.values())
            parsed_record: dict = {}
            is_duplicate_containers_in_line, is_reversed = \
                self.find_duplicate_containers(is_duplicate_containers_in_line, is_reversed, row, keys_list,
                                               values_list, sign_repeat_container, parsed_record, context, set_index,
                                               dict_last_value, index, last_container_seal_and_container_dict)
            if not is_duplicate_containers_in_line and set_index:
                self.update_values_duplicate_containers(set_index, index, list_data, is_reversed, sign_repeat_container)
            last_container_seal_and_container_dict[row["container_number"]] = row["container_seal"]
        return list_data


if __name__ == '__main__':
    parsed_data: Verim = Verim(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_reversed=True))
    del parsed_data
