import re
import sys
from __init__ import *
from typing import Union
from fuzzywuzzy import fuzz
from datetime import datetime
from BaseLine import BaseLine


class Admiral(BaseLine):

    dict_columns_position: Dict[str, Union[None, int]] = {
        "number_pp": None,
        "container_size_and_type": None,
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

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        self.logger_write.info(f"Will parse date in value {parsing_row.rsplit(':', 1)[1]}...")
        month: List[str] = parsing_row.rsplit(':', 1)[1].strip().split()
        month_digit: Union[None, int] = None
        if month[1] in month_list:
            month_digit = (month_list.index(month[1]) + 1) % 12
            if month_digit == 0:
                month_digit = 12
        date: datetime = datetime.strptime(f'{month[2].strip()}-{str(month_digit)}-{month[0].strip()}', "%Y-%m-%d")
        context["date"] = str(date.date())
        self.logger_write.info(f"context now is {context}")

    def parse_content_before_table(self, column: str, columns: tuple, parsing_row: str, list_month: list,
                                   context: dict, row: list) -> None:
        """
        Parsing from row the date, ship name and voyage in the cells before the table.
        """
        if re.findall(column, parsing_row):
            if DICT_CONTENT_BEFORE_TABLE[columns] == "date":
                self.parse_date(parsing_row, list_month, context, row)
            elif DICT_CONTENT_BEFORE_TABLE[columns] == "ship_voyage":
                self.parse_ship_and_voyage(parsing_row, row, column, context, "ship_voyage")

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str):
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        ship_and_voyage_list: list = parsing_row.replace(column, "").strip().rsplit(' ', 1)
        context["ship"] = ship_and_voyage_list[0].strip()
        context["voyage"] = re.sub(r'[^\w\s]', '', ship_and_voyage_list[1])
        self.logger_write.info(f"context now is {context}")

    def get_content_before_table(self, row, context, list_month) -> None:
        """
        Getting the date, ship name and voyage in the cells before the table.
        """
        try:
            for parsing_row in row:
                for columns in DICT_CONTENT_BEFORE_TABLE:
                    for column in columns:
                        self.parse_content_before_table(column, columns, parsing_row, list_month, context, row)
        except (IndexError, ValueError):
            self.logger_write.error("Error code 3: Date or Ship or Voyage not in cells")
            print("3", file=sys.stderr)
            sys.exit(3)

    def get_columns_position(self, row: list) -> None:
        """
        Get the position of each column in the file to process the row related to that column.
        """
        for index, column in enumerate(row):
            for columns in DICT_HEADERS_COLUMN_ENG:
                for column_eng in columns:
                    if column == column_eng:
                        self.dict_columns_position[DICT_HEADERS_COLUMN_ENG[columns]] = index

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        # ToDo:
        """
        if row[self.dict_columns_position["container_size_and_type"]]:
            parsed_record['container_size'] = \
                int(re.findall(r"\d{2}", row[self.dict_columns_position["container_size_and_type"]].strip())[0])
            parsed_record['container_type'] = \
                re.findall("[A-Z a-z]{1,4}", row[self.dict_columns_position["container_size_and_type"]].strip())[0]
        else:
            parsed_record['container_size'] = row[self.dict_columns_position["shipper_country"]].strip()
            parsed_record['container_type'] = row[self.dict_columns_position["shipper_country"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]].strip()

    def parse_row(self, index: int, row: list, context: dict, list_data: list) -> None:
        """
        Getting values from columns in a table.
        """
        self.logger_write.info(f'row {index} is {row}')
        parsed_record: dict = {}
        self.add_frequently_changing_keys(row, parsed_record)
        parsed_record['shipper_country'] = row[self.dict_columns_position["shipper_country"]].strip()
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

    def get_content_in_table(self, row: list, index: int, list_data: list, context: dict) -> list:
        """
        Getting values from columns in a table. And also catching the error.
        """
        try:
            self.parse_row(index, row, context, list_data)
        except (IndexError, ValueError):
            self.logger_write.error(f"Error code 5: error processing in row {index + 1}!")
            print(f"5_in_row_{index + 1}", file=sys.stderr)
            sys.exit(5)
        finally:
            return list_data

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or \
            (not self.is_digit(row[self.dict_columns_position["number_pp"]]) and
             not row[self.dict_columns_position["container_size_and_type"]] and
             not row[self.dict_columns_position["container_number"]] and
             row[self.dict_columns_position["consignment"]])

    def check_errors_in_header(self, row: list, context: dict) -> None:
        """
        # ToDo: Writing
        """
        self.check_errors_in_columns([context.get("ship", None), context.get("voyage", None),
                                      context.get("date", None)], context,
                                     "Error code 3: Keys (ship, voyage or date) not in cells", 3)
        self.get_columns_position(row)
        self.check_errors_in_columns(list(self.dict_columns_position.values()), self.dict_columns_position,
                                     "Error code 2: Column not in file or changed", 2)

    def get_content_from_file(self, file_name_save: str) -> List[dict]:
        """
        Complete processing of the file.
        """
        rows: list
        context: dict
        rows, context = self.create_parsed_data_and_context(file_name_save, self.input_file_path)
        list_data: List[dict] = []
        list_columns: List[str] = []
        for keys in list(DICT_HEADERS_COLUMN_ENG.keys()):
            list_columns.extend(iter(keys))
        for index, row in enumerate(rows):
            try:
                if fuzz.partial_ratio(row, list_columns) > 50:
                    self.check_errors_in_header(row, context)
                elif self.is_table_starting(row):
                    list_data = self.get_content_in_table(row, index, list_data, context)
            except TypeError:
                continue
            finally:
                self.get_content_before_table(row, context, LIST_MONTH)
        return list_data

    def main(self, is_need_duplicate_containers: bool = True, is_reversed: bool = False, sign: str = '') -> int:
        """
        Complete processing of the file. As well as deleting empty columns, rows and filling repeating containers
        with data, followed by saving the file in json.
        """
        file_name_save: str = self.remove_empty_columns_and_rows()
        list_data = self.get_content_from_file(file_name_save)
        if is_need_duplicate_containers:
            list_data = self.fill_data_with_duplicate_containers(list_data, sign, is_reversed=is_reversed)
        os.remove(file_name_save)
        self.write_data_in_file(list_data)
        return len(self.count_unique_containers(list_data))


if __name__ == '__main__':
    parsed_data = Admiral(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_reversed=True))
