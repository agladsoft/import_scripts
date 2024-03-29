import json
from __init__ import *
import requests


class Parsed:
    def __init__(self):
        self.url = "http://158.160.77.121:8004"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.logging = write_log(__file__)

    def body(self, row, line):
        data = {
            'line': line,
            'consignment': row['consignment'],
            'direction': 'import'

        }
        return data

    def get_result(self, row, line):
        body = self.body(row, line)
        body = json.dumps(body)
        try:
            self.logging.info(f'Отправка запроса в микро-сервис по {body}')
            answer = requests.post(self.url, data=body, headers=self.headers,timeout=120)
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

    def write_port(self, row, port):
        row['is_auto_tracking'] = True
        if port:
            row['is_auto_tracking_ok'] = True
            row['tracking_seaport'] = port
        else:
            row['is_auto_tracking_ok'] = False
            row['tracking_seaport'] = None

    def add_new_columns(self, row):
        if "enforce_auto_tracking" not in row:
            row['is_auto_tracking'] = None


LINES = ['REEL SHIPPING', 'СИНОКОР РУС ООО', 'HEUNG-A LINE CO., LTD', 'MSC', 'SINOKOR', 'SINAKOR', 'SKR', 'sinokor']
IMPORT = ['импорт', 'import']


class ParsedDf:
    def __init__(self, df):
        self.df = df
        self.url = "http://158.160.77.121:8004"
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.logging = write_log(__file__)

    def get_direction(self, direction):
        if direction.lower() in IMPORT:
            return 'import'
        else:
            return 'export'

    def body(self, row):
        data = {
            'line': row.get('line'),
            'consignment': row.get('consignment'),
            'direction': self.get_direction(row.get('direction','not'))

        }
        return data

    def get_result(self, row):
        body = self.body(row)
        body = json.dumps(body)
        try:
            answer = requests.post(self.url, data=body, headers=self.headers, timeout=120)
            if answer.status_code != 200:
                return None
            result = answer.json()
        except Exception as ex:
            self.logging.info(f'Ошибка {ex}')
            return None
        return result

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
                port = self.get_result(row)
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

    def check_line(self, line):
        if line not in LINES:
            return True
        return False

    def add_new_columns(self):
        if "enforce_auto_tracking" not in self.df.columns:
            self.df['is_auto_tracking'] = None
