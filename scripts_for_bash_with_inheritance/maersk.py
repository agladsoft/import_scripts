import os
import logging
import re
import sys
import datetime
import json
from __init__ import logger
from economou import WriteDataFromCsvToJsonEconomou

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]


class WriteDataFromCsvToJsonMaersk(WriteDataFromCsvToJsonEconomou):

    def write_ship_and_voyage(self, line, context):
        i = 0
        for parsing_line in line:
            if re.findall('[A-Za-z0-9]', parsing_line):
                logging.info(f"Will parse ship and trip in value '{parsing_line}'...")
                if i == 1: context['ship'] = parsing_line.strip()
                elif i == 2: context['voyage'] = parsing_line.strip()
                i += 1
                logging.info(f"context now is {context}")

    def write_date(self, line, context, xlsx_data):
        for parsing_line in line:
            if re.findall('[0-9]', parsing_line):
                try:
                    logging.info(u"Checking if we are on common line with number...")
                    date = datetime.datetime.strptime(parsing_line.rsplit(' ')[0], "%d-%B-%Y")
                    context['date'] = str(date.date())
                except Exception:
                    logger.info("Date not in cells!")
                    sys.exit(3)

    def read_file_name_save(self, file_name_save, line_file=__file__):
        lines, context, parsed_data = self.create_parsed_data_and_context(file_name_save, input_file_path, line_file)
        for ir, line in enumerate(lines):
            if (re.findall('Bill of Lading', line[0]) and re.findall('Shipper', line[1]) and re.findall('Consignee', line[2])) or \
                    self.activate_var:
                self.activate_var = True
                parsed_record = dict()
                if self.activate_row_headers:
                    self.check_error_in_columns([context.get("ship", False), context.get("voyage", False),
                                                 context.get("date", False)],
                                                "Keys (ship or voyage or date) not in cells!", 3)
                    self.activate_row_headers = False
                    for ir, column_position in enumerate(line):
                        if re.findall('Bill of Lading', column_position): self.ir_consignment = ir
                        elif re.findall('Shipper', column_position): self.ir_shipper = ir
                        elif re.findall('Consignee', column_position): self.ir_consignee = ir
                        elif re.findall('Container', column_position): self.ir_container_number = ir
                        elif re.findall('Weight', column_position): self.ir_weight_goods = ir
                        elif re.findall('Places', column_position): self.ir_package_number = ir
                        elif re.findall('Type', column_position): self.ir_container_size_and_type = ir
                    self.check_error_in_columns(
                        [self.ir_consignment, self.ir_shipper, self.ir_consignee, self.ir_container_number,
                         self.ir_weight_goods, self.ir_package_number, self.ir_container_size_and_type],
                        "Column not in file or changed!", 2)
                else:
                    try:
                        true_line = bool(line[self.ir_consignment]), bool(line[self.ir_shipper]), \
                                    bool(line[self.ir_consignee]), bool(line[self.ir_container_number]), \
                                    bool(line[self.ir_container_size_and_type]), bool(line[self.ir_weight_goods])
                        logging.info(u'line {} is {}'.format(ir, line))
                        if true_line == (True, True, True, False, True, False):
                            logging.info(u"Ok, line looks common...")
                            context['consignment'] = line[self.ir_consignment].strip()
                            context['shipper'] = line[self.ir_shipper].strip()
                            context['consignee'] = line[self.ir_consignee].strip()
                            city_split_comma = [i for i in line[self.ir_consignee].replace('\n', ' ').split(',')][1:]
                            city_split_point = [i for i in line[self.ir_consignee].replace('\n', ' ').split('.')][1:]
                            context['city'] = " ".join(city_split_comma).strip() if city_split_comma else " ".join(
                                city_split_point).strip()
                        elif true_line == (False, False, True, True, True, True) or true_line == (False, False, False, True,
                                                                                                  True, True):
                            context['container_number'] = line[self.ir_container_number].strip()
                            container_size = re.findall("\d{2}", line[self.ir_container_size_and_type].strip())[0]
                            container_type = re.findall("[A-Z a-z]{1,4}", line[self.ir_container_size_and_type].strip())[0]
                            context['container_size'] = int(container_size)
                            context['container_type'] = container_type
                            context['goods_weight'] = float(line[self.ir_weight_goods]) if line[self.ir_weight_goods] else None
                            context['package_number'] = line[self.ir_package_number].strip() if line[self.ir_package_number] else None
                            record = self.merge_two_dicts(context, parsed_record)
                            logging.info(u"record is {}".format(record))
                            parsed_data.append(record)
                        elif true_line == (True, False, False, False, False, False):
                            context['goods_name_rus'] = line[self.ir_goods_name_rus].strip()
                            record = self.merge_two_dicts(context, parsed_record)
                            logging.info(u"record is {}".format(record))
                            parsed_data.append(record)
                        if bool(re.findall('(^\d{9}$|^[a-zA-Z]{3}\d{6}$|^[a-zA-Z]{6}\d{3}$|\d{2}[a-zA-Z]\d{6}|^[a-zA-Z]{'
                                           '1}[0-9a-zA-Z]{6}[_]\d{3}|\d{1}[a-zA-Z]{2}\d{6}|[0-9a-zA-Z]{7}[_]\d{3}|\d{1}['
                                           '0-9a-zA-Z]{8})', line[self.ir_consignment])):
                            context['goods_name_rus'] = ''
                        context['original_file_name'] = os.path.basename(self.input_file_path)
                        context['original_file_parsed_on'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    except Exception:
                        logger.info(f"Error processing in row {ir}!")
                        sys.exit(5)
            else:
                for name in line:
                    if re.findall('MANIFEST', name):
                        self.write_ship_and_voyage(line, context)
                    elif re.findall('Port of Loading', name):
                        self.write_date(line, context, False)

        return parsed_data

    def write_list_with_containers_in_file(self, parsed_data):
        if len(parsed_data) == 0:
            logger.info("Length list equals 0!")
            sys.exit(4)
        basename = os.path.basename(input_file_path)
        output_file_path = os.path.join(output_folder, f'{basename}.json')
        print(f"output_file_path is {output_file_path}")
        parsed_data_2 = []
        with open(output_file_path, 'w', encoding='utf-8') as f:
            parsed_data_2.extend(row for row in parsed_data if row['goods_name_rus'])
            json.dump(parsed_data_2, f, ensure_ascii=False, indent=4)
        set_container = {item['container_number'] for item in parsed_data_2}
        logging.info(f"Length is unique containers {len(set_container)}")
        return len(set_container)

    def __call__(self, *args, **kwargs):
        file_name_save = self.remove_empty_columns_and_rows()
        parsed_data = self.read_file_name_save(file_name_save)
        os.remove(file_name_save)
        return self.write_list_with_containers_in_file(parsed_data)


if __name__ == '__main__':
    parsed_data = WriteDataFromCsvToJsonMaersk(input_file_path, output_folder)
    print(parsed_data())
