import os
import sys
from admiral import Admiral, telegram


class Zim(Admiral):
    pass


if __name__ == '__main__':
    parsed_data: Zim = Zim(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_reversed=True))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
