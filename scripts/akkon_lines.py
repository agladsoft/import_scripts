import re
import sys
from __init__ import *
from typing import Union
from admiral import Admiral


class AkkonLines(Admiral):

    dict_columns_position: Dict[str, Union[None, int]] = Admiral.dict_columns_position
    del dict_columns_position["container_size_and_type"]
    dict_columns_position["container_size"] = None
    dict_columns_position["container_type"] = None

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str) -> None:
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
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]].strip()
        parsed_record['shipper_country'] = row[self.dict_columns_position["tracking_country"]].strip()


if __name__ == '__main__':
    parsed_data: AkkonLines = AkkonLines(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
