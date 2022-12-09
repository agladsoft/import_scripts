import logging

console = logging.StreamHandler()
logger = logging.getLogger("loggger")
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console)
logger.setLevel(logging.INFO)

month_list = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь",
              "октябрь", "ноябрь", "декабрь", 'ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА',
              'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ', 'ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ',
              'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ']

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