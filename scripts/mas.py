import re
import os
import sys
from cosco import Cosco


class Mas(Cosco):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or \
            (not self.is_digit(row[self.dict_columns_position["number_pp"]]) and
             re.findall(r"\w{4}\d{7}", row[self.dict_columns_position["container_number"]]))


if __name__ == '__main__':
    parsed_data: Mas = Mas(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
