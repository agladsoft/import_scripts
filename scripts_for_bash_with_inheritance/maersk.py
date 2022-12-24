import re
import sys
from __init__ import *
from arkas import Arkas
from typing import Union
from admiral import Admiral
from evergreen import Evergreen
from datetime import datetime


class Maersk(Evergreen):
    dict_columns_position: Dict[str, Union[None, int]] = Arkas.dict_columns_position
    del dict_columns_position["number_pp"]
    del dict_columns_position["container_size"]
    del dict_columns_position["container_type"]
    del dict_columns_position["container_seal"]
    del dict_columns_position["shipper_country"]
    del dict_columns_position["goods_tnved"]
    dict_columns_position["container_size_and_type"] = None

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        Arkas.parse_ship_and_voyage(self, parsing_row, row, column, context, key, 1, 2)

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%d-%B-%Y" format.
        """
        self.logger_write.info(u"Checking if we are on common line with number...")
        date = datetime.strptime(parsing_row.rsplit(' ')[0], "%d-%B-%Y")
        context['date'] = str(date.date())
        self.logger_write.info(f"context now is {context}")

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list) -> None:
        Admiral.parse_content_before_table(self, column, columns, parsing_row, list_month, context, row)

    def check_errors_in_header(self, row: list, context: dict, no_need_column: str = "goods_tnved") -> None:
        Evergreen.check_errors_in_header(self, row, context, "goods_name_rus")

    def is_table_starting(self, row: list) -> tuple:
        """
        Understanding when a headerless table starts.
        """
        return bool(row[self.dict_columns_position["consignment"]]), \
            bool(row[self.dict_columns_position["shipper"]]), \
            bool(row[self.dict_columns_position["consignee"]]), \
            bool(row[self.dict_columns_position["container_number"]]), \
            bool(row[self.dict_columns_position["container_size_and_type"]]), \
            bool(row[self.dict_columns_position["goods_weight"]])

    def parse_row(self, index: int, row: list, context: dict, list_data: list) -> None:
        """
        Getting values from columns in a table.
        """
        self.logger_write.info(f'row {index} is {row}')
        parsed_record: dict = {}
        is_need_row: Tuple[bool] = self.is_table_starting(row)
        if is_need_row == (True, True, True, False, True, False):
            self.get_participants(row, context)
        elif is_need_row in [(False, False, True, True, True, True), (False, False, False, True, True, True)]:
            self.get_container_data(row, context, parsed_record, list_data)
        elif is_need_row == (True, False, False, False, False, False):
            context['goods_name_rus'] = row[self.dict_columns_position["goods_name_rus"]].strip()
            self.merge_data(context, parsed_record, list_data)
        if bool(re.findall(r'(^\d{9}$|^[a-zA-Z]{3}\d{6}$|^[a-zA-Z]{6}\d{3}$|\d{2}[a-zA-Z]\d{6}|^[a-zA-Z][0-9a-zA-Z]'
                           r'{6}_\d{3}|\d[a-zA-Z]{2}\d{6}|[0-9a-zA-Z]{7}_\d{3}|\d[0-9a-zA-Z]{8})',
                           row[self.dict_columns_position["consignment"]])):
            context['goods_name_rus'] = ''
        context['original_file_name'] = os.path.basename(self.input_file_path)
        context['original_file_parsed_on'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def get_container_data(self, row: list, context: dict, parsed_record: dict, list_data: list) -> None:
        """
        # ToDo:
        """
        context['container_number'] = row[self.dict_columns_position["container_number"]].strip()
        container_size: list = re.findall(r"\d{2}", row[self.dict_columns_position["container_size_and_type"]].strip())
        container_type: list = re.findall(r"[A-Z a-z]{1,4}",
                                          row[self.dict_columns_position["container_size_and_type"]].strip())
        context['container_size'] = int(container_size[0])
        context['container_type'] = container_type[0]
        context['goods_weight'] = float(row[self.dict_columns_position["goods_weight"]]) \
            if row[self.dict_columns_position["goods_weight"]] else None
        context['package_number'] = row[self.dict_columns_position["package_number"]].strip() \
            if row[self.dict_columns_position["package_number"]] else None
        self.merge_data(context, parsed_record, list_data)

    def get_participants(self, row: list, context: dict) -> None:
        """
        # ToDo:
        """
        context['consignment'] = row[self.dict_columns_position["consignment"]].strip()
        context['shipper'] = row[self.dict_columns_position["shipper"]].strip()
        context['consignee'] = row[self.dict_columns_position["consignee"]].strip()
        city_split_comma: list = list(row[self.dict_columns_position["consignee"]].replace('\n', ' ').split(','))[1:]
        city_split_point: list = list(row[self.dict_columns_position["consignee"]].replace('\n', ' ').split('.'))[1:]
        context['city'] = " ".join(city_split_comma).strip() if city_split_comma else " ".join(city_split_point).strip()

    def merge_data(self, context: dict, parsed_record: dict, list_data: list) -> None:
        """
        # ToDo:
        """
        record: dict = self.merge_two_dicts(context, parsed_record)
        self.logger_write.info(f"record is {record}")
        list_data.append(record)


if __name__ == '__main__':
    parsed_data = Maersk(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
