from __init__ import *
from arkas import Arkas
from silmar import Silmar
from major import Major, telegram
from akkon_lines import AkkonLines


class MajorCargoService(Silmar):
    dict_columns_position: Dict[str, Union[None, int]] = Silmar.dict_columns_position
    dict_columns_position["number_pp"] = None

    def is_table_starting(self, row: list) -> bool:
        """
        Understanding when a headerless table starts.
        """
        return AkkonLines.is_table_starting(self, row)

    def parse_date(self, parsing_row: str, month_list: list, context: dict, row: list) -> None:
        """
        Getting the date in "%Y-%m-%d" format.
        """
        Arkas.parse_date(self, parsing_row, month_list, context, row)

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str,
                              index_ship: int = 0, index_voyage: int = 1) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        Major.parse_ship_and_voyage(self, parsing_row, row, column, context, key, index_voyage=2)

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from Arkas.
        """
        Silmar.add_frequently_changing_keys(self, row, parsed_record)


if __name__ == '__main__':
    parsed_data: MajorCargoService = MajorCargoService(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(is_need_duplicate_containers=False))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
