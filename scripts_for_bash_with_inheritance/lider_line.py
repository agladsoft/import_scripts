import sys
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
        "goods_weight": 10,
        "package_number": 9,
        "goods_name_rus": 7,
        "shipper": 13,
        "shipper_country": 14,
        "consignee": 15,
        "consignment": 11,
        "city": 16
    }

    def process_row(self, row: list, index: int, list_data: List[dict], context: dict, list_columns: list,
                    coefficient_of_header: int) -> None:
        """
        The process of processing each line.
        """
        if self.get_probability_of_header(row, list_columns) > coefficient_of_header:
            self.check_errors_in_header(row, context)
        elif self.is_table_starting(row):
            self.get_content_in_table(row, index, list_data, context)
        elif "английское" in row and "класс опасности / ООН" in row:
            self.change_index_of_column(10, 11, 12, 14, 15, 16, 17)
        elif "русское" in row and "английское" not in row:
            self.change_index_of_column(8, 9, 10, 12, 13, 14, 15)
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
        self.dict_columns_position["goods_weight"] = goods_weight
        self.dict_columns_position["consignment"] = consignment
        self.dict_columns_position["shipper"] = shipper
        self.dict_columns_position["shipper_country"] = shipper_country
        self.dict_columns_position["consignee"] = consignee
        self.dict_columns_position["city"] = city


if __name__ == '__main__':
    parsed_data: LiderLine = LiderLine(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    print(parsed_data.main())
    del parsed_data
