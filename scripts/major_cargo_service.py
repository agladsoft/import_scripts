import os
import sys
from major import Major, telegram
from akkon_lines import AkkonLines


class MajorCargoService(Major):

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return AkkonLines.is_table_starting(self, row)

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        Major.parse_ship_and_voyage(self, parsing_row, row, column, context, key, index_voyage=2)


if __name__ == '__main__':
    parsed_data: MajorCargoService = MajorCargoService(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(sign='*'))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
