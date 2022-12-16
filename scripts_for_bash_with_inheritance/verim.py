import os
import logging
import sys
import re
from __init__ import month_list
from WriteDataFromCsvToJson import WriteDataFromCsvToJson


input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonVerim(WriteDataFromCsvToJson):

    def read_file_name_save(self, file_name_save, line_file=__file__):
        lines, context, parsed_data = self.create_parsed_data_and_context(file_name_save, input_file_path, line_file)
        for ir, line in enumerate(lines):
            if (re.findall('№', line[0]) and re.findall('Статус', line[1]) and re.findall('Номер контейнера', line[2])) or self.activate_var:
                self.activate_var = True
                parsed_record = dict()
                if self.activate_row_headers:
                    self.check_error_in_columns([context.get("ship", False), context.get("voyage", False),
                                                 context.get("date", False)],
                                                "Keys (ship or voyage or date) not in cells!", 3)
                    self.activate_row_headers = False
                    for ir, column_position in enumerate(line):
                        if re.findall('Статус', column_position): self.ir_container_size_and_type = ir
                        elif re.findall('Город', column_position): self.ir_city = ir
                        elif re.findall('Страна отправителя', column_position): self.ir_shipper_country = ir
                        self.define_header_table_containers(ir, column_position, 'Коносамент', 'Пломба',
                                                            'Номер контейнера',
                                                            'Вес брутто', 'мест', 'Наименование груза',
                                                            'Отправитель', 'Получатель',
                                                            '№ п/п')
                    self.check_error_in_columns([self.ir_city, self.ir_container_size_and_type, self.ir_shipper_country,
                                                 self.ir_consignment, self.ir_number_plomb, self.ir_container_number,
                                                 self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus,
                                                 self.ir_shipper, self.ir_consignee, self.ir_number_pp],
                                                "Column not in file or changed!", 2)
                else:
                    if self.isDigit(line[self.ir_number_pp].replace('/', '.')) or line[self.ir_goods_name_rus]:
                        try:
                            logging.info(u'line {} is {}'.format(ir, line))
                            try:
                                container_size = re.findall("\d{2}", line[self.ir_container_size_and_type].strip())[0]
                                container_type = re.findall("[A-Z a-z]{1,4}", line[self.ir_container_size_and_type].strip())[0]
                                parsed_record['container_size'] = int(container_size)
                                parsed_record['container_type'] = container_type
                            except IndexError:
                                parsed_record['container_size'] = ''
                                parsed_record['container_type'] = ''
                            parsed_record['shipper_country'] = line[self.ir_shipper_country].strip()
                            parsed_record['city'] = line[self.ir_city].strip()
                            parsed_record['container_seal'] = line[self.ir_number_plomb]
                            record = self.add_value_from_data_to_list(line, self.ir_container_number,
                                                                      self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus,
                                                                      self.ir_shipper, self.ir_consignee,
                                                                      self.ir_consignment, parsed_record, context)
                            logging.info(u"record is {}".format(record))
                            parsed_data.append(record)
                        except Exception:
                            logging.info(f"Error processing in row {ir}!")
                            print(f"5_in_row_{ir + 1}", file=sys.stderr)
                            sys.exit(5)
            else:
                self.write_data_before_containers_in_one_column(line, context, month_list, "ВЫГРУЗКА ГРУЗА С")
        return parsed_data

    @staticmethod
    def update_values_duplicate_containers(set_index, index, parsed_data, is_reversed):
        key_list = list(parsed_data[list(set_index)[0]].keys())
        val_list = list(parsed_data[list(set_index)[0]].values())

        positions = [i for i, d in enumerate(val_list) if d == '']
        for index_container in list(set_index):
            for position in positions:
                parsed_data[index_container][key_list[position]] = parsed_data[index][key_list[position]] \
                    if is_reversed else parsed_data[index - len(set_index) - 1][key_list[position]]
            set_index.pop()

    @staticmethod
    def find_duplicate_containers(is_duplicate_containers_in_line, is_reversed, *args):
        for key, value in zip(args[1], args[2]):
            if value == args[3]:
                try:
                    args[6].add(args[8])
                    is_duplicate_containers_in_line = True
                    if args[0]["container_seal"] == list(args[9].values())[-1] and list(args[9].keys())[-1] != '':
                        is_reversed = False
                    args[5][key] = args[7][key]
                except (KeyError, IndexError):
                    continue
            else:
                args[4][key] = value
            if value != args[3]:
                args[7][key] = value
        return is_duplicate_containers_in_line, is_reversed

    def write_duplicate_containers_in_dict(self, parsed_data, values, **kwargs):
        context = {}
        list_last_value = {}
        set_index = set()
        is_reversed = True
        last_container_seal_and_container_dict = {}
        for index, line in enumerate(parsed_data):
            if line["container_number"] == '' and line["container_seal"] == '' and line['container_type'] == '' \
                    and line['container_size'] == '':
                logging.info(f'Container_seal is empty on row {index}')
                print(f"5_in_row_{index + 1}", file=sys.stderr)
                sys.exit(5)
            is_duplicate_containers_in_line = False
            keys_list = list(line.keys())
            values_list = list(line.values())
            parsed_record = {}
            is_duplicate_containers_in_line, is_reversed = \
                self.find_duplicate_containers(is_duplicate_containers_in_line, is_reversed, line, keys_list,
                                               values_list, values, parsed_record, context, set_index,
                                               list_last_value, index, last_container_seal_and_container_dict)
            if not is_duplicate_containers_in_line and set_index:
                self.update_values_duplicate_containers(set_index, index, parsed_data, is_reversed)
            last_container_seal_and_container_dict[line["container_number"]] = line["container_seal"]
        return parsed_data

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        parsed_data = self.write_duplicate_containers_in_dict(parsed_data, '')
        os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonVerim(input_file_path, output_folder)
    print(parsed_data())