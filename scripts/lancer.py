import os
import sys
from admiral import Admiral


class Lancer(Admiral):
    pass


if __name__ == '__main__':
    parsed_data: Lancer = Lancer(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
