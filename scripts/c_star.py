import os
import sys
from mas import MAS


class CStart(MAS):
    pass


if __name__ == '__main__':
    parsed_data: CStart = CStart(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
