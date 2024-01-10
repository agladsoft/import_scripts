import os
import sys
from evergreen import Evergreen, telegram


class Major(Evergreen):
    pass


if __name__ == '__main__':
    parsed_data: Major = Major(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(sign='*'))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
