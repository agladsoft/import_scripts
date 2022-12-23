import sys
from __init__ import *
from arkas import Arkas
from typing import Union
from akkon_lines import AkkonLines


class Economou(Arkas):

    dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    dict_columns_position["city"] = None

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        AkkonLines.add_frequently_changing_keys(self, row, parsed_record)


if __name__ == '__main__':
    parsed_data = Economou(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
