import os
import sys
from lider_line import LiderLine


class UcakLine(LiderLine):
    pass


if __name__ == '__main__':
    parsed_data: UcakLine = UcakLine(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
