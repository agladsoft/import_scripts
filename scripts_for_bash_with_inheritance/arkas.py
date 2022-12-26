import re
import sys
import math
from __init__ import *
from typing import Union
from akkon_lines import AkkonLines
from datetime import datetime, timedelta


class Arkas(AkkonLines):

    dict_columns_position: Dict[str, Union[None, int]] = AkkonLines.dict_columns_position
    del dict_columns_position["city"]

    @staticmethod
    def convert_xlsx_datetime_to_date(xlsx_datetime: float) -> str:
        """
        Convert date to %Y-%m-%d from xlsx value.
        """
        days: float
        portion: float
        temp_date: datetime = datetime(1899, 12, 30)
        (days, portion) = math.modf(xlsx_datetime)
        delta_days: timedelta = timedelta(days=days)
        secs: int = int(24 * 60 * 60 * portion)
        delta_seconds: timedelta = timedelta(seconds=secs)
        time: datetime = (temp_date + delta_days + delta_seconds)
        return time.strftime("%Y-%m-%d")

    def parse_date_format_russia(self, parsing_row, context):
        """
        Getting the date in "%d.%m-%y" format.
        """
        self.logger_write.info(f"Will parse date in value {parsing_row}...")
        try:
            date: datetime = datetime.strptime(parsing_row, "%d.%m.%Y")
        except ValueError:
            date: datetime = datetime.strptime(parsing_row, "%d.%m.%y")
        context['date'] = str(date.date())
        self.logger_write.info(f"context now is {context}")

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        for parsing_row in row:
            if re.findall(r'\d{4}-\d{1,2}-\d{1,2}', parsing_row):
                self.logger_write.info(f"Will parse date in value {parsing_row}...")
                date: datetime = datetime.strptime(parsing_row.replace("T00:00:00.000", ""), "%Y-%m-%d")
                context['date'] = str(date.date())
                self.logger_write.info(f"context now is {context}")
                break
            elif re.findall(r'\d{1,2}[.]\d{1,2}[.]\d{2,4}', parsing_row):
                self.parse_date_format_russia(parsing_row, context)
                break
            elif re.findall(r'[0-9]', parsing_row):
                context['date'] = self.convert_xlsx_datetime_to_date(float(parsing_row))
                break

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        index: int = 0
        for ship_voyage in row:
            position: int = list(DICT_CONTENT_BEFORE_TABLE.values()).index("ship_voyage_in_other_cells")
            if re.findall(list(DICT_CONTENT_BEFORE_TABLE.keys())[position][0], ship_voyage):
                if index == index_ship:
                    context['ship'] = ship_voyage.strip()
                elif index == index_voyage:
                    context['voyage'] = ship_voyage.strip()
                index += 1
        self.logger_write.info(f"context now is {context}")

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        city: list = list(row[self.dict_columns_position["consignee"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()
        parsed_record['shipper_country'] = row[self.dict_columns_position["shipper_country"]].strip()


if __name__ == '__main__':
    parsed_data: Arkas = Arkas(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
    del parsed_data
