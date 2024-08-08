import json
import time
import sys
from __init__ import *
from database import DataBase
from typing import Optional

database = DataBase()


def get_line_unified(item: dict, line_name: str):
    for key, value in item.items():
        if line_name in value:
            return key
    return line_name


LINES = database.get_list_unified_lines()


class Parsed:
    def __init__(self):
        self.url = f"http://{os.environ['IP_ADDRESS_CONSIGNMENTS']}:8004"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.logging = write_log(__file__)

    def body(self, row, line):
        line_unified = get_line_unified(LINES, line.upper())
        return {
            'line': line_unified,
            'consignment': row['consignment'],
            'direction': 'import',
        }

    def get_result(self, row, line):
        body = self.body(row, line)
        body = json.dumps(body)
        try:
            self.logging.info(f'Отправка запроса в микро-сервис по {body}')
            answer = requests.post(self.url, data=body, headers=self.headers, timeout=120)
            self.logging.info(f'Получен ответ по запросу {body}')
            if answer.status_code != 200:
                return None
            result = answer.json()
        except Exception as ex:
            self.logging.info(f'Ошибка {ex}')
            return None
        return result

    def get_port(self, row, line):
        self.add_new_columns(row)
        port = self.get_result(row, line)
        self.write_port(row, port)

    @staticmethod
    def write_port(row, port):
        row['is_auto_tracking'] = True
        if port:
            row['is_auto_tracking_ok'] = True
            row['tracking_seaport'] = port
        else:
            row['is_auto_tracking_ok'] = False
            row['tracking_seaport'] = None

    @staticmethod
    def add_new_columns(row):
        if "enforce_auto_tracking" not in row:
            row['is_auto_tracking'] = None


# LINES = ['REEL SHIPPING', 'СИНОКОР РУС ООО', 'HEUNG-A LINE CO., LTD', 'MSC', 'SINOKOR', 'SINAKOR', 'SKR', 'sinokor']
IMPORT = ['импорт', 'import']


class ParsedDf:
    def __init__(self, df):
        self.df = df
        self.url = f"http://{os.environ['IP_ADDRESS_CONSIGNMENTS']}:8004"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.logging = write_log(__file__)

    @staticmethod
    def get_direction(direction):
        return 'import' if direction.lower() in IMPORT else 'export'

    def body(self, row):
        line_unified = get_line_unified(LINES, row.get('line', '').upper())
        return {
            'line': line_unified,
            'consignment': row.get('consignment'),
            'direction': self.get_direction(row.get('direction', 'not')),
        }

    def get_port_with_recursion(self, number_attempts: int, row) -> Optional[str]:
        if number_attempts == 0:
            return None
        try:
            body = self.body(row)
            body = json.dumps(body)
            response = requests.post(self.url, data=body, headers=self.headers, timeout=120)
            response.raise_for_status()
            return response.json()
        except Exception as ex:
            self.logging.error(f"Exception is {ex}")
            time.sleep(30)
            number_attempts -= 1
            self.get_port_with_recursion(number_attempts, row)

    def get_port(self):
        self.add_new_columns()
        self.logging.info("Запросы к микросервису")
        data = {}
        for index, row in self.df.iterrows():
            if row.get('tracking_seaport') is not None:
                continue
            if not row.get('enforce_auto_tracking', False):
                continue
            if row.get('consignment', False) not in data:
                data[row.get('consignment')] = {}
                number_attempts = 3
                port = self.get_port_with_recursion(number_attempts, row)
                self.write_port(index, port)
                try:
                    data[row.get('consignment')].setdefault('tracking_seaport',
                                                            self.df.get('tracking_seaport')[index])
                    data[row.get('consignment')].setdefault('is_auto_tracking',
                                                            self.df.get('is_auto_tracking')[index])
                    data[row.get('consignment')].setdefault('is_auto_tracking_ok',
                                                            self.df.get('is_auto_tracking_ok')[index])
                except KeyError as ex:
                    self.logging.info(f'Ошибка при получение ключа из DataFrame {ex}')
            else:
                tracking_seaport = data.get(row.get('consignment')).get('tracking_seaport') if data.get(
                    row.get('consignment')) is not None else None
                is_auto_tracking = data.get(row.get('consignment')).get('is_auto_tracking') if data.get(
                    row.get('consignment')) is not None else None
                is_auto_tracking_ok = data.get(row.get('consignment')).get('is_auto_tracking_ok') if data.get(
                    row.get('consignment')) is not None else None
                self.df.at[index, 'tracking_seaport'] = tracking_seaport
                self.df.at[index, 'is_auto_tracking'] = is_auto_tracking
                self.df.at[index, 'is_auto_tracking_ok'] = is_auto_tracking_ok
        self.logging.info('Обработка закончена')

    def write_port(self, index, port):
        self.df.at[index, 'is_auto_tracking'] = True
        if port:
            self.df.at[index, 'is_auto_tracking_ok'] = True
            self.df.at[index, 'tracking_seaport'] = port
        else:
            self.df.at[index, 'is_auto_tracking_ok'] = False

    @staticmethod
    def check_line(line):
        return line not in LINES

    def add_new_columns(self):
        if "enforce_auto_tracking" not in self.df.columns:
            self.df['is_auto_tracking'] = None
