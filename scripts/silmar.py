import re
import os
import sys
from cma_cgm import CmaCgm
from typing import Union, Dict
from evergreen import Evergreen


class Silmar(CmaCgm, Evergreen):

    dict_columns_position: Dict[str, Union[None, int]] = CmaCgm.dict_columns_position
    del dict_columns_position["number_pp"]
    dict_columns_position["city"] = None

    def check_errors_in_header(self, row: list, context: dict, no_need_columns: list = None) -> None:
        Evergreen.check_errors_in_header(self, row, context, no_need_columns=["city", "goods_tnved"])

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%d-%m-%Y" format.
        """
        date = re.findall(r'\d{1,2}[.]\d{1,2}[.]\d{2,4}', os.path.basename(sys.argv[1]))[0]
        self.parse_date_format_russia(date, context)

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return bool(re.findall(r"\w{4}\d{7}", row[self.dict_columns_position["container_number"]]))

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]].strip() \
            if self.dict_columns_position["city"] else None
        parsed_record['shipper_country'] = row[self.dict_columns_position["shipper_country"]].strip()
        parsed_record['goods_tnved'] = row[self.dict_columns_position["goods_tnved"]] \
            if self.dict_columns_position["goods_tnved"] else None


if __name__ == '__main__':
    parsed_data: Silmar = Silmar(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
