import os
import sys
from cosco import Cosco


class MAAS(Cosco):
    pass


if __name__ == '__main__':
    parsed_data: MAAS = MAAS(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
