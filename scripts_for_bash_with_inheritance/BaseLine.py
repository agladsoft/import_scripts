import re
import csv
import sys
import json
import datetime
import pandas as pd
from re import Match
from __init__ import *
from typing import Union
from pandas.io.parsers import read_csv


class WriteDataFromCsvToJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseLine):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class BaseLine:
    def __init__(self, input_file_path, output_folder, line_file):
        self.input_file_path: str = input_file_path
        self.output_folder: str = output_folder
        self.logger_write: Logger = write_log(line_file)
        self.line_file = line_file

    @staticmethod
    def is_digit(x: str) -> bool:
        """
        Checks if a value is a number.
        """
        try:
            float(re.sub(r'(?<=\d) (?=\d)', '', x))
            return True
        except ValueError:
            return False

    @staticmethod
    def merge_two_dicts(x: Dict, y: Dict) -> dict:
        """
        Merges two dictionaries.
        """
        z: Dict = x.copy()  # start with keys and values of x
        z.update(y)  # modifies z with keys and values of y
        return z

    def check_error_in_columns(self, list_columns: list, message: str, error_code: int) -> None:
        """
        Checks for the presence of all columns in the header.
        """
        if not all(i for i in list_columns if i is False):
            self.logger_write.info(message)
            self.logger_write.info(list_columns)
            print(f"{error_code}", file=sys.stderr)
            sys.exit(error_code)

    def add_value_from_data_to_list(self, line: list, ir_container_number: int, ir_weight_goods: int,
                                    ir_package_number: int, ir_goods_name_rus: int, ir_shipper: int, ir_consignee: int,
                                    ir_consignment: int, parsed_record: dict, context: dict) -> dict:
        """
        Adding values from a table to a dictionary.
        """
        container_number: str = re.sub(r'(?<=\w) (?=\d)', '', line[ir_container_number].strip())
        try:
            parsed_record['container_number'] = re.findall(r"\w{4}\d{7}", container_number)[0]
        except IndexError:
            parsed_record['container_number'] = container_number
        parsed_record['goods_weight'] = float(re.sub(" +", "", line[ir_weight_goods]).replace(',', '.')) if line[
            ir_weight_goods] else None
        parsed_record['package_number'] = int(float(line[ir_package_number])) if line[ir_package_number] else None
        parsed_record['goods_name_rus'] = line[ir_goods_name_rus].strip()
        parsed_record['consignment'] = line[ir_consignment].strip()
        parsed_record['shipper'] = line[ir_shipper].strip()
        parsed_record['consignee'] = line[ir_consignee].strip()
        parsed_record['original_file_name'] = os.path.basename(self.input_file_path)
        parsed_record['original_file_parsed_on'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return self.merge_two_dicts(context, parsed_record)

    def remove_empty_columns_and_rows(self) -> str:
        """
        Removing empty lines and columns in a file.
        """
        file_name_save: str = f'{os.path.dirname(self.input_file_path)}' \
                              f'/{os.path.basename(self.input_file_path)}_empty_column_removed.csv'
        data: pd.Dataframe = read_csv(self.input_file_path)
        filtered_data_column: pd.Dataframe = data.dropna(axis=1, how='all')
        filtered_data_rows: pd.Dataframe = filtered_data_column.dropna(axis=0, how='all')
        filtered_data_rows.to_csv(file_name_save, index=False)
        return file_name_save

    def create_parsed_data_and_context(self, file_name_save: str, input_file_path: str) \
            -> Tuple[list, dict]:
        """
        The initial configuration file. Checking the file for the presence of a date at the beginning,
        assigning a terminal and a line.
        """
        self.logger_write.info(f'file is {os.path.basename(input_file_path)} {datetime.datetime.now()}')
        context: dict = dict(line=os.path.basename(self.line_file).replace(".py", ""))
        context['terminal'] = os.environ.get('XL_IMPORT_TERMINAL')
        date_previous: Match[str] | None = re.match(r'\d{2,4}.\d{1,2}', os.path.basename(file_name_save))
        date_previous: str = f'{date_previous.group()}.01' if date_previous else date_previous
        if date_previous is None:
            self.logger_write.info("Date not in file name!")
            print("1", file=sys.stderr)
            sys.exit(1)
        else:
            context['parsed_on'] = str(datetime.datetime.strptime(date_previous, "%Y.%m.%d").date())
        with open(file_name_save, newline='') as csvfile:
            rows: list = list(csv.reader(csvfile))
        return rows, context

    def define_is_equal_value_with_sign(self, keys_list: list, values_list: list, context: dict,
                                        list_last_value: dict, parsed_record: dict, sign_repeat_container: str,
                                        record: Union[None, dict] = None) -> Union[None, dict]:
        """
        Defining the current cell's signed equality defining a repeating container.
        """
        for key, value in zip(keys_list, values_list):
            if value == sign_repeat_container:
                try:
                    context[key] = list_last_value[key]
                except KeyError:
                    continue
            else:
                parsed_record[key] = value
            record: Union[None, dict] = self.merge_two_dicts(context, parsed_record)
            if value != sign_repeat_container:
                list_last_value[key] = value
        return record

    def fill_data_with_duplicate_containers(self, list_data: list, sign_repeat_container: str,
                                            is_reversed: bool) -> list:
        """
        Filling empty cells with data in repeating containers.
        """
        parsed_data_with_duplicate_containers: list = []
        context: dict = {}
        list_last_value: dict = {}
        list_data = reversed(list_data) if is_reversed else list_data
        for line in list_data:
            keys_list: list = list(line.keys())
            values_list: list = list(line.values())
            parsed_record: dict = {}
            record = self.define_is_equal_value_with_sign(keys_list, values_list, context, list_last_value,
                                                          parsed_record, sign_repeat_container)
            parsed_data_with_duplicate_containers.append(record)
        return parsed_data_with_duplicate_containers

    def count_unique_containers(self, list_data: List[dict]) -> set:
        """
        Counting unique containers.
        """
        set_container = set()
        for container in list_data:
            try:
                if container['container_number']:
                    set_container.add(container['container_number'])
            except KeyError:
                continue
        self.logger_write.info(f"Length is unique containers {len(set_container)}")
        return set_container

    def write_data_in_file(self, list_data: List[dict]) -> None:
        """
        Writing data to json.
        """
        if not list_data:
            self.logger_write.info("Length list equals 0!")
            print("4", file=sys.stderr)
            sys.exit(4)
        basename = os.path.basename(self.input_file_path)
        output_file_path = os.path.join(self.output_folder, f'{basename}.json')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(list_data, f, ensure_ascii=False, indent=4, cls=WriteDataFromCsvToJsonEncoder)