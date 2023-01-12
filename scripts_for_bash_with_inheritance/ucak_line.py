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