import json
import requests

LINES = ['REEL SHIPPING', 'СИНОКОР РУС ООО', 'HEUNG-A LINE CO., LTD', 'MSC', 'SINOKOR']


class Parsed:
    def __init__(self):
        # self.df = df
        self.url = "http://10.23.4.203:8004"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def body(self, row,line):
        data = {
            'line': line,
            'consignment': row['consignment'],
            'direction': 'import'

        }
        return data

    def get_result(self, row,line):
        body = self.body(row,line)
        body = json.dumps(body)
        answer = requests.post(self.url, data=body, headers=self.headers)
        if answer.status_code != 200:
            return None
        result = answer.json()
        return result

    def get_port(self,row,line):
        self.add_new_columns(row)
        port = self.get_result(row,line)
        self.write_port(row, port)

    def write_port(self,row, port):
        row['is_auto_tracking'] = True
        if port:
            row['is_auto_tracking_ok'] = True
            row['tracking_seaport'] = port
        else:
            row['is_auto_tracking_ok'] = False


    def add_new_columns(self,row):
        row['is_auto_tracking'] = None