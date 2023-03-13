import os
import sys
from cosco import Cosco


class Medkon(Cosco):
    pass


if __name__ == '__main__':
    parsed_data: Medkon = Medkon(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
