import re
import sys
from __init__ import *
from typing import Union
from admiral import Admiral


class AkkonLines(Admiral):

    dict_columns_position: Dict[str, Union[bool, int]] = {
        "number_pp": False,
        "container_size": False,
        "container_type": False,
        "container_number": False,
        "container_seal": False,
        "goods_weight": False,
        "package_number": False,
        "goods_name_rus": False,
        "shipper": False,
        "shipper_country": False,
        "consignee": False,
        "consignment": False,
        "city": False,
    }

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list) -> None:
        """
        Parsing from row the date, ship name and voyage in the cells before the table.
        """
        if re.findall(column, parsing_row) and DICT_CONTENT_BEFORE_TABLE[columns] == "date":
            self.parse_date(parsing_row, list_month, context)
        elif re.findall(column, parsing_row) and DICT_CONTENT_BEFORE_TABLE[columns] == "ship_voyage":
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

    def parse_row(self, index: int, row: list, context: dict, list_data: list) -> None:
        """
        Getting values from columns in a table.
        """
        self.logger_write.info(f'line {index} is {row}')
        parsed_record: dict = {'container_size': int(float(row[self.dict_columns_position["container_size"]].strip())),
                               'container_type': row[self.dict_columns_position["container_type"]].strip(),
                               'shipper_country': row[self.dict_columns_position["shipper_country"]].strip(),
                               'city': row[self.dict_columns_position["city"]].strip()}
        record: dict = self.add_value_from_data_to_list(row, self.dict_columns_position["container_number"],
                                                        self.dict_columns_position["goods_weight"],
                                                        self.dict_columns_position["package_number"],
                                                        self.dict_columns_position["goods_name_rus"],
                                                        self.dict_columns_position["shipper"],
                                                        self.dict_columns_position["consignee"],
                                                        self.dict_columns_position["consignment"], parsed_record,
                                                        context)
        self.logger_write.info(f"record is {record}")
        list_data.append(record)


if __name__ == '__main__':
    parsed_data = AkkonLines(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
