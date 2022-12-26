import os
import sys
from cosco import Cosco


class RcLine(Cosco):
    pass


if __name__ == '__main__':
    parsed_data: RcLine = RcLine(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
