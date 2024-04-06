import os
import sys
from verim import Verim
from __init__ import *


class Lam(Verim):
    pass


if __name__ == '__main__':
    parsed_data: Lam = Lam(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
