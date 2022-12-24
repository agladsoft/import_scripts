import os
import sys
from admiral import Admiral


class Cosco(Admiral):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]].replace('/', '.'))


if __name__ == '__main__':
    parsed_data: Cosco = Cosco(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main(is_need_duplicate_containers=False))
