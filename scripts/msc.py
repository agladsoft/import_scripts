import re
import sys
import contextlib
from __init__ import *
from cma_cgm import CmaCgm
from admiral import Admiral
from typing import Union, Dict
from evergreen import Evergreen


class Msc(CmaCgm, Evergreen):

    dict_columns_position: Dict[str, Union[None, int]] = Evergreen.dict_columns_position
    del dict_columns_position["container_size"]
    del dict_columns_position["container_type"]
    dict_columns_position["container_size_and_type"] = None

    def check_errors_in_header(self, row: list, context: dict, no_need_columns: list = None) -> None:
        """
        Checking for columns in the entire document, counting more than just columns on the same line.
        """
        Evergreen.check_errors_in_header(self, row, context, no_need_columns=["tnved"])

    def parse_ship_and_voyage2(self, row: list, context: dict) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        index: int = 0
        for parsing_row in row:
            if re.findall('[A-Za-z0-9]', parsing_row):
                self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
                if index == 0:
                    if "рейс" in parsing_row:
                        ship_and_voyage: list = parsing_row.split("рейс")
                        context["ship_name"] = self.remove_keys_in_data(ship_and_voyage[0])
                        context['voyage'] = self.remove_keys_in_data(ship_and_voyage[1])
                    else:
                        context["ship_name"] = parsing_row.strip()
                elif index == 1:
                    context['voyage'] = self.remove_keys_in_data(parsing_row)
                index += 1
                self.logger_write.info(f"context now is {context}")

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list, ship_voyage: str = "ship_voyage") -> None:
        """
        Parsing from row the date, ship name and voyage in the cells before the table.
        """
        if re.findall(column, parsing_row):
            if DICT_CONTENT_BEFORE_TABLE[columns] == "shipment_date":
                self.parse_date(parsing_row, list_month, context, row)
            elif DICT_CONTENT_BEFORE_TABLE[columns] == "ship_voyage" and not context.get("ship_name") and not \
                    context.get('voyage'):
                self.parse_ship_and_voyage2(row, context)
            elif DICT_CONTENT_BEFORE_TABLE[columns] == "ship_voyage_msc":
                self.parse_ship_and_voyage(parsing_row, row, column, context, "ship_name")

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        with contextlib.suppress(IndexError):
            Admiral.parse_ship_and_voyage(self, parsing_row, row, column, context, key)

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        container_number: str = re.sub(r'(?<=\w) (?=\d)', '',
                                       row[self.dict_columns_position["container_number"]].strip())
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or (
                not self.is_digit(row[self.dict_columns_position["number_pp"]])
                and bool(re.findall(r"\w{4}\d{7}", container_number))
                and row[self.dict_columns_position["container_size_and_type"]])

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = \
            int(re.findall(r"\d{2}", row[self.dict_columns_position["container_size_and_type"]].strip())[0])
        parsed_record['container_type'] = \
            re.findall("[A-Z a-z]{1,4}", row[self.dict_columns_position["container_size_and_type"]].strip())[0]
        city: list = list(row[self.dict_columns_position["consignee_name"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()
        parsed_record["tracking_country"] = row[self.dict_columns_position["tracking_country"]].strip()
        parsed_record["tnved"] = row[self.dict_columns_position["tnved"]] \
            if self.dict_columns_position["tnved"] else None

    def is_duplicate_container_in_row(self, value: str, sign_repeat_container: str, key: str) -> bool:
        """
        Method inheritance from BaseLine.
        """
        return CmaCgm.is_duplicate_container_in_row(value, sign_repeat_container, key)

    def is_not_duplicate_container_in_row(self, value: str, sign_repeat_container: str) -> bool:
        """
        Method inheritance from BaseLine.
        """
        return CmaCgm.is_not_duplicate_container_in_row(value, sign_repeat_container)


if __name__ == '__main__':
    parsed_data: Msc = Msc(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
