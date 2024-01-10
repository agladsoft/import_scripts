import re
import os
import sys
from cosco import Cosco, telegram


class MAS(Cosco):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return self.is_digit(row[self.dict_columns_position["number_pp"]]) or \
            (not self.is_digit(row[self.dict_columns_position["number_pp"]]) and
             re.findall(r"\w{4}\d{7}", row[self.dict_columns_position["container_number"]])
             or row[self.dict_columns_position["consignment"]])

    def transfer_data_non_merged_cells(self, row: list, rows: list) -> None:
        """
        Transferring data from the following lines to the previous ones.
        Examples:

                   TKRU4362300	  10119505	 3750	118.84
                                                    602.33
                                                    9219.2
        44	40HC			                        77.5

        If the cells were merged, the row would look like this

        44	40HC   TKRU4362300	  10119505	 3750	118.84
                                                    602.33
                                                    9219.2
        			                                77.5

        """
        if not self.is_digit(row[self.dict_columns_position["number_pp"]]) \
                and re.findall(r"\w{4}\d{7}", row[self.dict_columns_position["container_number"]]):
            for next_row in rows:
                if next_row[self.dict_columns_position["number_pp"]] \
                        and next_row[self.dict_columns_position["container_size_and_type"]] \
                        and not next_row[self.dict_columns_position["container_number"]] \
                        and next_row[self.dict_columns_position["consignment"]]:
                    row[self.dict_columns_position["number_pp"]] = next_row[self.dict_columns_position["number_pp"]]
                    row[self.dict_columns_position["container_size_and_type"]] = \
                        next_row[self.dict_columns_position["container_size_and_type"]]
                    next_row[self.dict_columns_position["number_pp"]] = ""
                    next_row[self.dict_columns_position["container_size_and_type"]] = ""
                    break


if __name__ == '__main__':
    parsed_data: MAS = MAS(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка при обработке файла {ex}')
        sys.exit(6)
    del parsed_data
