import os
from typing import Dict, Tuple, List
from logging import Logger, getLogger, StreamHandler, INFO, FileHandler


def write_log(line_file: str) -> Logger:
    full_dir_name_logging = f'{os.environ.get("XL_IDP_ROOT")}/logging'
    if not os.path.exists(full_dir_name_logging):
        os.mkdir(full_dir_name_logging)
    logger_handler: FileHandler = FileHandler(filename=f'{full_dir_name_logging}/'
                                                       f'{os.path.basename(line_file).replace(".py", "")}.log')
    logger_write: Logger = getLogger("write_logger")
    if logger_write.hasHandlers():
        logger_write.handlers.clear()
    logger_write.addHandler(logger_handler)
    logger_write.setLevel(INFO)
    return logger_write


def output_log() -> Logger:
    logger: Logger = getLogger("loggger")
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(StreamHandler())
    logger.setLevel(INFO)
    return logger


LIST_MONTH: List[str] = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
                         "октября", "ноября", "декабря", "январь", "февраль", "март", "апрель", "май", "июнь", "июль",
                         "август", "сентябрь", "октябрь", "ноябрь", "декабрь", 'ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ',
                         'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ', 'ЯНВАРЬ',
                         'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ',
                         'ДЕКАБРЬ']

DICT_HEADERS_COLUMN_ENG: Dict[Tuple, str] = {
    ("№ п/п",): "number_pp",
    ("Статус",): "container_size_and_type",
    ("Тип",): "container_type",
    ("Размер",): "container_size",
    ("Номер контейнера",): "container_number",
    ("Пломба",): "container_seal",
    ("Вес брутто (кг)",): "goods_weight",
    ("Количество мест",): "package_number",
    ("Наименование груза",): "goods_name_rus",
    ("ТНВЭД",): "goods_tnved",
    ("Отправитель",): "shipper",
    ("Страна отправителя",): "shipper_country",
    ("Получатель",): "consignee",
    ("Коносамент",): "consignment",
    ("Город",): "city"
}

DICT_CONTENT_BEFORE_TABLE: Dict[Tuple, str] = {
    ("ДАТА ПРИХОДА", "дата прихода", "Дата прихода"): "date",
    ("ВЫГРУЗКА ГРУЗА С", "Название судна",): "ship_voyage",
    ("[A-Z0-9]",): "ship_voyage_in_other_cells",
    # ("Название судна",): "ship_voyage"
}
