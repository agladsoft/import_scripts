from __init__ import *
from typing import Union
from cma_cgm import CmaCgm
from akkon_lines import AkkonLines


class LiderLine(CmaCgm):

    dict_columns_position: Dict[str, Union[None, int]] = {
        "number_pp": 0,
        "container_size": 2,
        "container_type": 3,
        "container_number": 1,
        "container_seal": 5,
        "goods_weight_with_package": 10,
        "package_number": 9,
        "goods_name": 7,
        "shipper_name": 13,
        "tracking_country": 14,
        "consignee_name": 15,
        "consignment": 11,
        "city": 16,
    }

    def check_errors_in_header(self, row: list, context: dict, no_need_columns: list = None) -> None:
        """
        Checking for columns in the entire document, counting more than just columns on the same line.
        """
        if no_need_columns is None:
            no_need_columns = []
        self.check_errors_in_columns(
            list_columns=[context.get("ship_name"), context.get("voyage"), context.get("shipment_date")],
            dict_columns=context,
            message="Error code 3: Keys (ship, voyage or date) not in cells",
            error_code=3
        )
        if "Наименование товара на русском" in row:
            self.get_columns_position(row)
        dict_columns_position = self.dict_columns_position.copy()
        for delete_column in no_need_columns:
            del dict_columns_position[delete_column]
        self.check_errors_in_columns(
            list_columns=list(dict_columns_position.values()),
            dict_columns=dict_columns_position,
            message="Error code 2: Column not in file or changed",
            error_code=2
        )

    def process_row(self, row: list, rows: list, index: int, list_data: List[dict], context: dict, list_columns: list,
                    coefficient_of_header: int) -> None:
        """
        The process of processing each line.
        """
        if self.get_probability_of_header(row, list_columns) > coefficient_of_header:
            self.check_errors_in_header(row, context)
        elif self.is_table_starting(row):
            self.get_content_in_table(row, rows, index, list_data, context)
        elif "английское" in row and "класс опасности / ООН" in row:
            self.change_index_of_column(10, 11, 12, 14, 15, 16, 17)
        elif "русское" in row and "английское" not in row:
            self.change_index_of_column(8, 9, 10, 12, 13, 14, 15)
        elif "Страна" in row:
            self.change_index_of_column(9, 10, 11, 13, 14, 16, 17)
        else:
            self.get_content_before_table(row, context, LIST_MONTH)

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Method inheritance from AkkonLines.
        """
        AkkonLines.add_frequently_changing_keys(self, row, parsed_record)

    def change_index_of_column(self, package_number: int, goods_weight: int, consignment: int, shipper: int,
                               shipper_country: int, consignee: int, city: int) -> None:
        """
        Changing the indexes of columns in the header.
        """
        self.dict_columns_position["package_number"] = package_number
        self.dict_columns_position["goods_weight_with_package"] = goods_weight
        self.dict_columns_position["consignment"] = consignment
        self.dict_columns_position["shipper_name"] = shipper
        self.dict_columns_position["tracking_country"] = shipper_country
        self.dict_columns_position["consignee_name"] = consignee
        self.dict_columns_position["city"] = city


if __name__ == '__main__':
    parsed_data: LiderLine = LiderLine(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main())
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError,KeyError) as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {parsed_data.input_file_path}')
        sys.exit(6)
    del parsed_data
