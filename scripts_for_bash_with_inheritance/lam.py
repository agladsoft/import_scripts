import os
import sys
from verim import WriteDataFromCsvToJsonVerim

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonLam(WriteDataFromCsvToJsonVerim):

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save, __file__)
        parsed_data = self.write_duplicate_containers_in_dict(parsed_data, '')
        os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonLam(input_file_path, output_folder)
    print(parsed_data())