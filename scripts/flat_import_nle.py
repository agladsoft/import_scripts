import os
import re
import sys
import json
import contextlib
import numpy as np
import pandas as pd
from typing import Union
from pandas import DataFrame
from datetime import datetime
from __init__ import *

headers_eng: dict = {
    "date": "shipment_date",
    "ship": "ship_name",
    "goods_name_rus": "goods_name",
    "shipper": "shipper_name",
    "consignee": "consignee_name",
    "count": "container_count",
    "shipper_country": "tracking_country",
    "goods_weight": "goods_weight_with_package",
    "shipper_seaport": "tracking_seaport",
    "goods_tnved": "tnved"
}


class ImportNLE(object):
    def __init__(self, input_file_path: str, output_folder: str):
        self.input_file_path: str = input_file_path
        self.output_folder: str = output_folder

    @staticmethod
    def change_type_and_values(df: DataFrame) -> None:
        """
        Change data types or changing values.
        """
        with contextlib.suppress(Exception):
            df['shipment_date'] = df['shipment_date'].dt.date.astype(str)
            df[['expeditor']] = df[['expeditor']].apply(lambda x: x.fillna('Нет данных'))

    def add_new_columns(self, df: DataFrame) -> None:
        """
        Add new columns.
        """
        date_previous: Union[re.Match[str], None] = re.match(r'\d{2,4}.\d{1,2}', os.path.basename(self.input_file_path))
        date_previous: str = f'{date_previous.group()}.01' if date_previous else date_previous
        if date_previous is None:
            telegram(f'Отсутствует дата в наименование файла {self.input_file_path}')
            sys.exit(1)
        else:
            df['parsed_on'] = str(datetime.strptime(date_previous, "%Y.%m.%d").date())
        df['original_file_name'] = os.path.basename(self.input_file_path)
        df['original_file_parsed_on'] = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def write_to_json(self, parsed_data: list) -> None:
        """
        Write data to json.
        """
        basename: str = os.path.basename(self.input_file_path)
        output_file_path: str = os.path.join(self.output_folder, f'{basename}.json')
        with open(f"{output_file_path}", 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=4)

    def main(self) -> None:
        """
        The main function where we read the Excel file and write the file to json.
        """
        df: DataFrame = pd.read_excel(self.input_file_path, dtype={"ИНН": str, "voyage": str})
        df = df.dropna(axis=0, how='all')
        df = df.rename(columns=headers_eng)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        self.add_new_columns(df)
        self.change_type_and_values(df)
        df = df.replace({np.nan: None, "NaT": None})
        self.write_to_json(df.to_dict('records'))


import_nw: ImportNLE = ImportNLE(sys.argv[1], sys.argv[2])
import_nw.main()
