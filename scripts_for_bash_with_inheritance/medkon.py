import os
import sys
from cosco import Cosco


class Medkon(Cosco):
    pass


if __name__ == '__main__':
    parsed_data = Medkon(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
