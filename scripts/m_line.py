import os
import re
import sys

from .admiral import Admiral, telegram
from .arkas import Arkas


class MLineAdmiral(Admiral):
    """
    MLine наследуется от Admiral с переопределением метода add_frequently_changing_keys.
    """

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        ship_and_voyage_list: list = parsing_row.replace(column, "").strip().rsplit(' ', 1)
        context["ship_name"] = ' '.join(ship_and_voyage_list).strip()
        context["voyage"] = 'нет данных'
        self.logger_write.info(f"context now is {context}")


class MLineArkas(Arkas):
    """
    Подкласс Arkas с переопределенным методом add_frequently_changing_keys.
    """

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]]
        parsed_record["tracking_country"] = row[self.dict_columns_position["tracking_country"]].strip()


if __name__ == '__main__':
    input_file = os.path.abspath(sys.argv[1])
    output_folder = sys.argv[2]

    try:
        parsed_data = MLineAdmiral(input_file, output_folder, __file__)
        print(parsed_data.main(is_reversed=True))
        del parsed_data

    except SystemExit as e:
        if e.code in [2, 3]:
            try:
                arkas_parser = MLineArkas(input_file, output_folder, __file__)
                result = arkas_parser.main(is_need_duplicate_containers=False)
                print(result)
                sys.exit(0)

            except Exception as arkas_ex:
                print("6", file=sys.stderr)
                telegram(f'Ошибка {arkas_ex} при обработке через Arkas')
                sys.exit(6)
        else:
            sys.exit(e.code)

    except Exception as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {input_file}')
        sys.exit(6)
