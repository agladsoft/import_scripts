import os
import sys
from admiral import Admiral


class Milaha(Admiral):
    pass


if __name__ == '__main__':
    parsed_data: Milaha = Milaha(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
