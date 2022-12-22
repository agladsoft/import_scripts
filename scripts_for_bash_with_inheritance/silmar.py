import os
import logging
import re
import sys
import datetime
from WriteDataFromCsvToJson import WriteDataFromCsvToJson

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonSilmar(WriteDataFromCsvToJson):

    @staticmethod
    def write_ship_and_voyage_silmar(line, context, key):
        for parsing_line in line:
            if re.findall('[A-Za-z0-9]', parsing_line):
                logging.info(f"Will parse ship and trip in value '{parsing_line}'...")
                context[key] = parsing_line.strip()
                logging.info(f"context now is {context}")

    @staticmethod
    def write_date_from_filename(file_name_save, context):
        try:
            date = re.findall('\d{1,2}[.]\d{1,2}[.]\d{2,4}', os.path.basename(file_name_save))[0]
            date = datetime.datetime.strptime(date, "%d.%m.%y")
            context['date'] = str(date.date())
        except IndexError:
            logging.info("There is no full date in the file name")

    def define_header_table_containers(self, ir, column_position, consignment, number_plomb, container_number,
                                       weight_goods, package_number, goods_name_rus, shipper, consignee, number_pp):
        if consignment == column_position: self.ir_consignment = ir
        elif re.findall(number_plomb, column_position): self.ir_number_plomb = ir
        elif re.findall(container_number, column_position): self.ir_container_number = ir
        elif re.findall(weight_goods, column_position): self.ir_weight_goods = ir
        elif re.findall(package_number, column_position): self.ir_package_number = ir
        elif re.findall(goods_name_rus, column_position): self.ir_goods_name_rus = ir
        elif shipper == column_position: self.ir_shipper = ir
        elif consignee == column_position: self.ir_consignee = ir
        elif re.findall(number_pp, column_position): self.ir_number_pp = ir

    def read_file_name_save(self, file_name_save, line_file=__file__):
        lines, context, parsed_data = self.create_parsed_data_and_context(file_name_save, input_file_path, line_file)
        self.write_date_from_filename(file_name_save, context)
        for ir, line in enumerate(lines):
            if (re.findall('Номер Контейнера', line[0]) and re.findall('Тип', line[1]) and
                re.findall('Размер', line[2])) or self.activate_var:
                self.activate_var = True
                parsed_record = {}
                if self.activate_row_headers:
                    for ir, column_position in enumerate(line):
                        self.activate_row_headers = False
                        if re.findall('Размер', column_position): self.ir_container_size = ir
                        elif re.findall('Тип', column_position): self.ir_container_type = ir
                        elif re.findall('Отправитель Город', column_position): self.ir_city = ir
                        elif re.findall('Код ТНВЭД', column_position): self.ir_goods_tnved = ir
                        elif re.findall('Отправитель Страна', column_position): self.ir_shipper_country = ir
                        self.define_header_table_containers(ir, column_position, 'Коносамент', 'Пломба',
                                                            'Номер Контейнера',
                                                            'Вес груза', 'Кол-во', 'Груз',
                                                            'Отправитель', 'Получатель',
                                                            '№')
                elif re.findall(r"\w{4}\d{7}", line[self.ir_container_number]):
                    logging.info(f'line {ir} is {line}')
                    parsed_record['container_size'] = int(float(line[self.ir_container_size]))
                    parsed_record['container_type'] = line[self.ir_container_type]
                    parsed_record['shipper_country'] = line[self.ir_shipper_country].strip()
                    parsed_record['city'] = line[self.ir_city]
                    parsed_record['goods_tnved'] = line[self.ir_goods_tnved]
                    record = self.add_value_from_data_to_list(line, self.ir_container_number,
                                                              self.ir_weight_goods, self.ir_package_number,
                                                              self.ir_goods_name_rus,
                                                              self.ir_shipper, self.ir_consignee,
                                                              self.ir_consignment, parsed_record, context)
                    logging.info(f"record is {record}")
                    parsed_data.append(record)
            else:
                for name in line:
                    if re.findall('Название парохода', name):
                        self.write_ship_and_voyage_silmar(line, context, 'ship')
                    elif re.findall('Номер рейса', name):
                        self.write_ship_and_voyage_silmar(line, context, 'voyage')

        return parsed_data

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonSilmar(input_file_path, output_folder)
    print(parsed_data())
