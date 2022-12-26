import os
import sys
from admiral import Admiral


class One(Admiral):
    pass


if __name__ == '__main__':
    parsed_data: One = One(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
