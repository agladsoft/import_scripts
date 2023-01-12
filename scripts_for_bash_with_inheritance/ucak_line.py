import os
import re
import sys
import logging
import datetime
import sys
from lider_line import WriteDataFromCsvToJsonLiderLine

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonUcakLine(WriteDataFromCsvToJsonLiderLine):

    @staticmethod
    def parse_date_format_russia(parsing_row, context):
        """
        Getting the date in "%d.%m-%y" format.
        """
        logging.info(f"Will parse date in value {parsing_row}...")
        try:
            date: datetime = datetime.datetime.strptime(parsing_row, "%d.%m.%Y")
        except ValueError:
            date: datetime = datetime.datetime.strptime(parsing_row, "%d.%m.%y")
        context['date'] = str(date.date())
        logging.info(f"context now is {context}")

    def write_date(self, line, context, xlsx_data):
        for parsing_row in line:
            if re.findall(r'\d{4}-\d{1,2}-\d{1,2}', parsing_row):
                logging.info(f"Will parse date in value {parsing_row}...")
                date = datetime.datetime.strptime(parsing_row.replace("T00:00:00.000", ""), "%Y-%m-%d")
                context['date'] = str(date.date())
                logging.info(f"context now is {context}")
                break
            elif re.findall(r'\d{1,2}[.]\d{1,2}[.]\d{2,4}', parsing_row):
                self.parse_date_format_russia(parsing_row, context)
                break
            elif re.findall(r'[0-9]', parsing_row):
                context['date'] = self.xldate_to_datetime(float(parsing_row))
                break

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        # if re.findall('xml', os.path.basename(file_name_save)):
        parsed_data = self.read_file_name_save_from_xml(file_name_save, __file__)
        # else:
        #     parsed_data = self.read_file_name_save(file_name_save)
        # os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonUcakLine(input_file_path, output_folder)
    print(parsed_data())