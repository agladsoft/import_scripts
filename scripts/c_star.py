import os
import sys
from mas import MAS


class CStart(MAS):
    pass


if __name__ == '__main__':
    parsed_data: CStart = CStart(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
