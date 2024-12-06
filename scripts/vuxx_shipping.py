import os
import sys
from __init__ import telegram
from reel_shipping import Evergreen


class VuxxShipping(Evergreen):
    pass


if __name__ == '__main__':
    parsed_data: VuxxShipping = VuxxShipping(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
