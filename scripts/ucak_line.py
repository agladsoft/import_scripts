import os
import sys
from lider_line import LiderLine, telegram


class UcakLine(LiderLine):
    pass


if __name__ == '__main__':
    parsed_data: UcakLine = UcakLine(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
