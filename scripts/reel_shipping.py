import os
import sys
from evergreen import Evergreen


class ReelShipping(Evergreen):

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip())) \
            if row[self.dict_columns_position["container_size"]] else '*'
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip() \
            if row[self.dict_columns_position["container_type"]] else '*'
        city: list = list(row[self.dict_columns_position["consignee"]].split(', '))[1:]
        parsed_record['city'] = " ".join(city).strip()
        parsed_record['goods_tnved'] = row[self.dict_columns_position["goods_tnved"]] \
            if self.dict_columns_position["goods_tnved"] else None
        parsed_record['shipper_country'] = row[self.dict_columns_position["shipper_country"]].strip() \
            if row[self.dict_columns_position["shipper_country"]] else '*'


if __name__ == '__main__':
    parsed_data: ReelShipping = ReelShipping(os.path.abspath(sys.argv[1]), sys.argv[2], __file__)
    try:
        print(parsed_data.main(sign="*"))
    except (ValueError, ImportError, IndexError, SyntaxError, TypeError, AttributeError) as ex:
        print("6", file=sys.stderr)
        sys.exit(6)
    del parsed_data
