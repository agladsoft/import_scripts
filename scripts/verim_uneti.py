import os
import sys
from verim import Verim, telegram


class VerimUneti(Verim):
    pass


if __name__ == '__main__':
    parsed_data: VerimUneti = VerimUneti(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
