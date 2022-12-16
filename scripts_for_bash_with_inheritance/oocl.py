import os
import logging
import re
import sys
from msc import WriteDataFromCsvToJsonMsc

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonOOCL(WriteDataFromCsvToJsonMsc):

    def write_ship_and_voyage(self, line, context):
        i = 0
        for parsing_line in line:
            if re.findall('[A-Za-z0-9]', parsing_line):
                logging.info(f"Will parse ship and trip in value '{parsing_line}'...")
                if i == 0:
                    ship_and_voyage_list = parsing_line.rsplit('рейс:', 1)
                    context['ship'] = ship_and_voyage_list[0].strip()
                    context['voyage'] = ship_and_voyage_list[1].strip()
                i += 1
                logging.info(f"context now is {context}")

    def read_file_name_save(self, file_name_save, line_file=__file__):
        lines, context, parsed_data = self.create_parsed_data_and_context(file_name_save, input_file_path, line_file)
        for ir, line in enumerate(lines):
            if (re.findall('№', line[0]) and re.findall('№ контейнера', line[1]) and re.findall('Размер', line[2])) or self.activate_var:
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
                        elif re.findall('Страна', column_position): self.ir_shipper_country = ir
                        self.define_header_table_containers(ir, column_position, '№ К/с', '№ пломбы',
                                                            'контейнера',
                                                            'Вес груза брт', 'Кол-во мест', 'Наименование заявленного груза \([(рус)]*\)',
                                                            'Грузоотправитель', 'Грузополуча',
                                                            '№ п/п')
                    self.check_error_in_columns(
                        [self.ir_container_size, self.ir_container_type, self.ir_shipper_country,
                         self.ir_consignment, self.ir_number_plomb, self.ir_container_number,
                         self.ir_weight_goods, self.ir_package_number, self.ir_goods_name_rus, self.ir_shipper,
                         self.ir_consignee, self.ir_number_pp], "Column not in file or changed!", 2)
                else:
                    if self.isDigit(line[self.ir_number_pp]) or (not self.isDigit(line[self.ir_number_pp]) and
                                                                 not line[self.ir_container_size] and
                                                                 not line[self.ir_container_number] and line[self.ir_consignment]):
                        try:
                            logging.info(u'line {} is {}'.format(ir, line))
                            parsed_record['container_size'] = int(float(line[self.ir_container_size].strip())) if line[self.ir_container_size] else ''
                            parsed_record['container_type'] = line[self.ir_container_type].strip()
                            parsed_record['shipper_country'] = line[self.ir_shipper_country].strip()
                            city = [i for i in line[self.ir_consignee].split(', ')][1:]
                            parsed_record['city'] = city[0].strip()
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
                for name in line:
                    if re.findall('Название судна', name):
                        self.write_ship_and_voyage(line, context)
                    elif re.findall('Дата прихода', name):
                        self.write_date(line, context, False)

        return parsed_data

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        parsed_data = self.write_duplicate_containers_in_dict(parsed_data, '', 'not_reversed')
        os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonOOCL(input_file_path, output_folder)
    print(parsed_data())