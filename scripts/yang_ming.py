import re
import os
import sys
from admiral import Admiral
from typing import Union, Dict


class YangMing(Admiral):

    dict_columns_position: Dict[str, Union[None, int]] = Admiral.dict_columns_position
    del dict_columns_position["tracking_country"]

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]].rsplit('(')[0]) or \
            (not row[self.dict_columns_position["number_pp"]] and row[self.dict_columns_position["container_seal"]] and
             row[self.dict_columns_position["goods_name"]])

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        container_size: str = re.findall(r"\d{2}",
                                         row[self.dict_columns_position["container_size_and_type"]].strip())[0]
        try:
            container_type: Union[str, None] = \
                re.findall("[A-Z a-z]{1,4}", row[self.dict_columns_position["container_size_and_type"]].strip())[0]
        except IndexError:
            container_type = None
        parsed_record['container_size'] = int(container_size)
        parsed_record['container_type'] = container_type
        shipper_country: list = list(row[self.dict_columns_position["shipper_name"]].split(', '))[-1:]
        parsed_record["tracking_country"] = shipper_country[0].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]].strip()


if __name__ == '__main__':
    parsed_data: YangMing = YangMing(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
