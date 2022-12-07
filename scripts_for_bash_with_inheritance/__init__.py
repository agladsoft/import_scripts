import logging

console = logging.StreamHandler()
logger = logging.getLogger("loggger")
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console)
logger.setLevel(logging.INFO)

list_column_eng = ["container_size", "container_type", "container_number", "goods_weight", "package_number",
                   "goods_name_rus", "consignment", "shipper", "consignee", "shipper_country", "city"]

# dict_headers_column_eng = {
#     ("Статус",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): "",
#     ("",): ""
# }