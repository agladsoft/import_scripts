import os
import sys
from rc_line import RcLine


class PjscTranscontainer(RcLine):
    pass


if __name__ == '__main__':
    parsed_data: PjscTranscontainer = PjscTranscontainer(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
