import os
import logging
import sys
import re
from __init__ import logger, month_list
from WriteDataFromCsvToJson import WriteDataFromCsvToJson

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonAkkonLines(WriteDataFromCsvToJson):

    def write_data_before_containers_in_one_column(self, line, context, month_list, var_name_ship):
        try:
            i = 0
            for parsing_line in line:
                if re.findall('ДАТА ПРИХОДА', parsing_line):
                    self.parse_date(parsing_line, month_list, context)
                elif re.findall(var_name_ship, parsing_line):
                    logging.info(f"Will parse ship and trip in value '{parsing_line}'...")
                    if var_name_ship == 'ВЫГРУЗКА ГРУЗА С': parsing_line = parsing_line.replace(var_name_ship, "").strip()
                    try:
                        ship_and_voyage_list = parsing_line.rsplit(' ', 1)
                        context['voyage'] = re.sub(r'[^\w\s]', '', ship_and_voyage_list[1])
                        context['ship'] = ship_and_voyage_list[0].strip()
                    except Exception:
                        if i == 0: context['ship'] = parsing_line.strip()
                        elif i == 1: context['voyage'] = parsing_line.strip()
                        i += 1
                    logging.info(f"context now is {context}")
        except Exception:
            logger.info("Date or Ship or Voyage not in cells!")
            sys.exit(3)

    def read_file_name_save(self, file_name_save, line_file=__file__):
        lines, context, parsed_data = self.create_parsed_data_and_context(file_name_save, input_file_path, line_file)
        for ir, line in enumerate(lines):
            if (re.findall('№', line[0]) and re.findall('Коносамент', line[1]) and re.findall('Номер контейнера', line[2])) or self.activate_var:
                self.activate_var = True
                parsed_record = dict()
                if self.activate_row_headers:
                    self.check_error_in_columns([context.get("ship", False), context.get("voyage", False),
                                                 context.get("date", False)],
                                                "Keys (ship or voyage or date) not in cells!", 3)
                    self.activate_row_headers = False
                    for ir, column_position in enumerate(line):
                        if re.findall('Размер', column_position): self.ir_container_size = ir
                        elif re.findall('Тип', column_position): self.ir_container_type = ir
                        elif re.findall('Город', column_position): self.ir_city = ir
                        elif re.findall('Страна отправителя', column_position): self.ir_shipper_country = ir
                        self.define_header_table_containers(ir, column_position, 'Коносамент', 'Пломба',
                                                            'Номер контейнера',
                                                            'Вес брутто', 'мест', 'Наименование груза',
                                                            'Отправитель', 'Получатель',
                                                            '№ п/п')
                    self.check_error_in_columns([self.ir_city, self.ir_container_size, self.ir_container_type, self.ir_shipper_country,
                                self.ir_consignment, self.ir_number_plomb, self.ir_container_number,
                                self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus, self.ir_shipper,
                                self.ir_consignee, self.ir_number_pp], "Column not in file or changed!", 2)
                else:
                    if self.isDigit(line[self.ir_number_pp]):
                        try:
                            logging.info(u'line {} is {}'.format(ir, line))
                            parsed_record['container_size'] = int(float(line[self.ir_container_size]))
                            parsed_record['container_type'] = line[self.ir_container_type].strip()
                            parsed_record['shipper_country'] = line[self.ir_shipper_country].strip()
                            parsed_record['city'] = line[self.ir_city].strip()
                            record = self.add_value_from_data_to_list(line, self.ir_container_number,
                                                                      self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus,
                                                                      self.ir_shipper, self.ir_consignee,
                                                                      self.ir_consignment, parsed_record, context)
                            logging.info(u"record is {}".format(record))
                            parsed_data.append(record)
                        except Exception:
                            logger.info(f"Error processing in row {ir}!")
                            sys.exit(5)
            else:
                if re.findall('ВЫГРУЗКА ГРУЗА С', line[0]) or re.findall('ДАТА ПРИХОДА', line[0]):
                    self.write_data_before_containers_in_one_column(line, context, month_list, "[A-Za-z0-9]")

        return parsed_data

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonAkkonLines(input_file_path, output_folder)
    print(parsed_data())
