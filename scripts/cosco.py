import os
import sys
from admiral import Admiral, telegram


class Cosco(Admiral):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]].replace('/', '.'))


if __name__ == '__main__':
    parsed_data: Cosco = Cosco(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
