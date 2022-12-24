import os
import sys
from evergreen import Evergreen


class Major(Evergreen):
    pass


if __name__ == '__main__':
    parsed_data: Major = Major(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(sign='*'))
