import re
import sys
from __init__ import *
from typing import Union
from admiral import Admiral


class AkkonLines(Admiral):

    dict_columns_position: Dict[str, Union[bool, int]] = {
        "number_pp": None,
        "container_size": None,
        "container_type": None,
        "container_number": None,
        "container_seal": None,
        "goods_weight": None,
        "package_number": None,
        "goods_name_rus": None,
        "shipper": None,
        "shipper_country": None,
        "consignee": None,
        "consignment": None,
        "city": None
    }

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str):
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        index: int = 0
        for ship_voyage in row:
            position: int = list(DICT_CONTENT_BEFORE_TABLE.values()).index("ship_voyage_in_other_cells")
            if re.findall(list(DICT_CONTENT_BEFORE_TABLE.keys())[position][0], ship_voyage):
                ship_voyage: str = ship_voyage.replace(column, "").strip()
                ship_and_voyage_list: list = ship_voyage.rsplit(' ', 1)
                try:
                    context["voyage"] = re.sub(r'[^\w\s]', '', ship_and_voyage_list[1])
                    context["ship"] = ship_and_voyage_list[0].strip()
                except IndexError:
                    context["ship"] = ship_voyage if index == 0 else context.get("ship")
                    context["voyage"] = ship_voyage if index == 1 else context.get("voyage")
                finally:
                    index += 1
        self.logger_write.info(f"context now is {context}")

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]])

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]].strip()


if __name__ == '__main__':
    parsed_data = AkkonLines(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
