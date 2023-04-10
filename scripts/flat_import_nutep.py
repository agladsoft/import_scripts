import csv
import datetime
import json
import os
import re
import sys

input_file_path = os.path.abspath(sys.argv[1])
output_folder = sys.argv[2]

with open(input_file_path, newline='') as csvfile:
    lines = csv.DictReader(csvfile)
    # headers = lines.fieldnames
    lines = list(lines)

headers = ["ship_name", "shipment_date",
           "terminal",
           "container_number",
           "container_size", "container_type", "goods_name", "consignment", "shipper_name", "consignee_name", "line", "voyage", "tracking_country", "goods_weight_brutto", "package_number", "city", "tracking_seaport",
           "tnved"
]
parsed_data = []
for line in lines:
    if not "".join(line.values()):
        continue
    parsed_record = {k: v for k, v in line.items() if k in headers}
    for key, value in parsed_record.items():
        if not value:
            parsed_record[key] = None
    parsed_record['terminal'] = os.environ.get('XL_IMPORT_TERMINAL')
    date_previous = re.match('\d{2,4}.\d{1,2}', os.path.basename(input_file_path))
    date_previous = f'{date_previous.group()}.01' if date_previous else date_previous
    if date_previous is None:
        raise Exception('Date not in file name!')
    else:
        parsed_record['parsed_on'] = str(datetime.datetime.strptime(date_previous, "%Y.%m.%d").date())
    parsed_record['original_file_name'] = os.path.basename(input_file_path)
    parsed_record['original_file_parsed_on'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    parsed_data.append(parsed_record)

basename = os.path.basename(input_file_path)
output_file_path = os.path.join(output_folder, f'{basename}.json')
with open(f"{output_file_path}", 'w', encoding='utf-8') as f:
    json.dump(parsed_data, f, ensure_ascii=False, indent=4)