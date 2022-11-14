import os
import logging
import sys
import re
from WriteDataFromCsvToJson import WriteDataFromCsvToJson

month_list = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря"]

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
                    for ir, column_position in enumerate(line):
                        self.activate_row_headers = False
                        if re.findall('Статус', column_position): self.ir_container_size_and_type = ir
                        elif re.findall('Город', column_position): self.ir_city = ir
                        elif re.findall('Страна отправителя', column_position): self.ir_shipper_country = ir
                        self.define_header_table_containers(ir, column_position, 'Коносамент', 'Пломба',
                                                            'Номер контейнера',
                                                            'Вес брутто', 'мест', 'Наименование груза',
                                                            'Отправитель', 'Получатель',
                                                            '№ п/п')
                else:
                    if self.isDigit(line[self.ir_number_pp].replace('/', '.')) or line[self.ir_goods_name_rus]:
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
                        # parsed_record['container_seal'] = line[self.ir_number_plomb]
                        record = self.add_value_from_data_to_list(line, self.ir_container_number,
                                                                  self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus,
                                                                  self.ir_shipper, self.ir_consignee,
                                                                  self.ir_consignment, parsed_record, context)
                        logging.info(u"record is {}".format(record))
                        parsed_data.append(record)
            else:
                self.write_data_before_containers_in_one_column(line, context, month_list, "ВЫГРУЗКА ГРУЗА С")
        return parsed_data

    # @staticmethod
    # def update_values_duplicate_containers(set_index, set_container_seal, parsed_record,
    #                                        parsed_data, parsed_data_with_duplicate_containers, record):
    #     key_list = list(parsed_data[list(set_index)[0]].keys())
    #     val_list = list(parsed_data[list(set_index)[0]].values())
    #
    #     positions = [i for i, d in enumerate(val_list) if d == '']
    #     for position in positions:
    #         parsed_data[list(set_index)[0]][key_list[position]] = parsed_record[key_list[position]]
    #     set_index.pop()
    #     set_container_seal.pop()
    #     parsed_data_with_duplicate_containers.append(record)
    #
    # def find_duplicate_containers(self, line, keys_list, values_list, values, parsed_record, context, set_index,
    #                               set_container_seal, list_last_value, index, is_duplicate_containers_in_line):
    #     for key, value in zip(keys_list, values_list):
    #         if value == values:
    #             try:
    #                 set_index.add(index)
    #                 set_container_seal.add(line["container_seal"])
    #                 is_duplicate_containers_in_line = True
    #                 context[key] = list_last_value[key]
    #             except KeyError:
    #                 continue
    #         else:
    #             parsed_record[key] = value
    #         if value != values:
    #             list_last_value[key] = value
    #         return self.merge_two_dicts(context, parsed_record)
    #
    # def write_duplicate_containers_in_dict(self, parsed_data, values):
    #     parsed_data_with_duplicate_containers = []
    #     context = {}
    #     list_last_value = {}
    #     set_index = set()
    #     set_container_seal = set()
    #     is_duplicate_containers_in_line = False
    #     for index, line in enumerate(parsed_data):
    #         keys_list = list(line.keys())
    #         values_list = list(line.values())
    #         parsed_record = {}
    #         record = self.find_duplicate_containers(line, keys_list, values_list, values, parsed_record, context, set_index,
    #                               set_container_seal, list_last_value, index, is_duplicate_containers_in_line)
    #         if not is_duplicate_containers_in_line:
    #             self.update_values_duplicate_containers(set_index, set_container_seal, parsed_record,
    #                                        parsed_data, parsed_data_with_duplicate_containers, record)
    #     return parsed_data_with_duplicate_containers

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        parsed_data = self.write_duplicate_containers_in_dict(parsed_data, '', 'not_reversed')
        # os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonVerim(input_file_path, output_folder)
    print(parsed_data())