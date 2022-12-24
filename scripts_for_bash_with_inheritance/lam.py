import os
import sys
from verim import Verim


class Lam(Verim):
    pass


if __name__ == '__main__':
    parsed_data: Lam = Lam(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
