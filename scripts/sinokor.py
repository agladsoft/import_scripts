import os
import sys
from verim import Verim


class Sinokor(Verim):
    pass


if __name__ == '__main__':
    parsed_data: Sinokor = Sinokor(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
