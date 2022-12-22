import re
import sys
import math
from __init__ import *
from typing import Union
from akkon_lines import AkkonLines
from datetime import datetime, timedelta


class Arkas(AkkonLines):

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
        "consignment": False
    }

    @staticmethod
    def convert_xlsx_datetime_to_date(xlsx_datetime):
        temp_date = datetime(1899, 12, 30)
        (days, portion) = math.modf(xlsx_datetime)
        delta_days = timedelta(days=days)
        secs = int(24 * 60 * 60 * portion)
        delta_seconds = timedelta(seconds=secs)
        time = (temp_date + delta_days + delta_seconds)
        return time.strftime("%Y-%m-%d")

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        for parsing_row in row:
            if re.findall(r'\d{4}-\d{1,2}-\d{1,2}', parsing_row):
                self.logger_write.info(f"Will parse date in value {parsing_row}...")
                date = datetime.strptime(parsing_row.replace("T00:00:00.000", ""), "%Y-%m-%d")
                context['date'] = str(date.date())
                self.logger_write.info(f"context now is {context}")
                break
            elif re.findall(r'\d{1,2}.\d{1,2}.\d{2,4}', parsing_row):
                self.logger_write.info(f"Will parse date in value {parsing_row}...")
                date = datetime.strptime(parsing_row, "%d.%m.%Y")
                context['date'] = str(date.date())
                self.logger_write.info(f"context now is {context}")
                break
            elif re.findall(r'[0-9]', parsing_row):
                context['date'] = self.convert_xlsx_datetime_to_date(float(parsing_row))

    def parse_row(self, index: int, row: list, context: dict, list_data: list) -> None:
        """
        Getting values from columns in a table.
        """
        self.logger_write.info(f'line {index} is {row}')
        parsed_record: dict = {'container_size': int(float(row[self.dict_columns_position["container_size"]].strip())),
                               'container_type': row[self.dict_columns_position["container_type"]].strip(),
                               'shipper_country': row[self.dict_columns_position["shipper_country"]].strip()}
        city: list = list(row[self.dict_columns_position["consignee"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()
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
    parsed_data = Arkas(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
