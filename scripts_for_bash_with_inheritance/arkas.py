import re
import sys
import math
from __init__ import *
from typing import Union
from akkon_lines import AkkonLines
from datetime import datetime, timedelta


class Arkas(AkkonLines):

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
        "consignment": None
    }

    @staticmethod
    def convert_xlsx_datetime_to_date(xlsx_datetime: float) -> str:
        days: float
        portion: float
        temp_date: datetime = datetime(1899, 12, 30)
        (days, portion) = math.modf(xlsx_datetime)
        delta_days: timedelta = timedelta(days=days)
        secs: int = int(24 * 60 * 60 * portion)
        delta_seconds: timedelta = timedelta(seconds=secs)
        time: datetime = (temp_date + delta_days + delta_seconds)
        return time.strftime("%Y-%m-%d")

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
            elif re.findall(r'\d{1,2}.\d{1,2}.\d{2,4}', parsing_row):
                self.logger_write.info(f"Will parse date in value {parsing_row}...")
                date: datetime = datetime.strptime(parsing_row, "%d.%m.%Y")
                context['date'] = str(date.date())
                self.logger_write.info(f"context now is {context}")
                break
            elif re.findall(r'[0-9]', parsing_row):
                context['date'] = self.convert_xlsx_datetime_to_date(float(parsing_row))

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        city: list = list(row[self.dict_columns_position["consignee"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()


if __name__ == '__main__':
    parsed_data = Arkas(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
