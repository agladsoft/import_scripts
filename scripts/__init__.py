import os
from typing import Dict, Tuple, List
from logging import Logger, getLogger, INFO, FileHandler


def write_log(line_file: str) -> Logger:
    full_dir_name_logging: str = f'{os.environ.get("XL_IDP_ROOT")}/logging'
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


LIST_MONTH: List[str] = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября",
                         "октября", "ноября", "декабря", "январь", "февраль", "март", "апрель", "май", "июнь", "июль",
                         "август", "сентябрь", "октябрь", "ноябрь", "декабрь", 'ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ',
                         'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ', 'ЯНВАРЬ',
                         'ФЕВРАЛЬ', 'МАРТ', 'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ', 'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ', 'ОКТЯБРЬ', 'НОЯБРЬ',
                         'ДЕКАБРЬ']

DICT_HEADERS_COLUMN_ENG: Dict[Tuple, str] = {
    ("№ п/п", "№", "№ пп."): "number_pp",
    ("Статус", "Тип", "Type"): "container_size_and_type",
    ("Тип",): "container_type",
    ("Размер",): "container_size",
    ("Номер контейнера", "№контейнера", "№ контейнера", "Container", "Номер Контейнера"): "container_number",
    ("Пломба", "№ пломбы", "№пломбы"): "container_seal",
    ("Вес брутто (кг)", "Вес груза", "Вес груза брт,кг", "Вес груза брт, кг", "Weight",
     "Вес, бр. груза", "Вес, бр. груза, кг"): "goods_weight",
    ("Количество мест", "Кол-во мест", "мест", "Кол-во", "Кол-во мест", "Places", "К-во мест", "К-во мест/вес товара",
     "Кол-о мест"): "package_number",
    ("Наименование груза", "Наименование заявленного груза", "Наименование заявленного груза (рус)", "Груз"):
        "goods_name_rus",
    ("ТНВЭД", "КОД ТНВЭД", "Код Тн ВЭД", "Российский Код ТНВЭД (10 знаков)", "Код ТНВЭД"): "goods_tnved",
    ("Отправитель", "Грузоотправитель", "Shipper To Order"): "shipper",
    ("Страна отправителя", "Страна грузоотправителя", "Страна отправления", "Страна", "Страна порта погрузки",
     "Страна затарки", "Страна погрузки", "Страна грузоотправителя", "Отправитель Страна"): "shipper_country",
    ("Получатель", "Грузополучатель", "Consignee Seal", "Грузополуча тель"): "consignee",
    ("Коносамент", "№ к/с", "№ Коносамента", "№коносамента", "Bill of Lading", "№ К/с"): "consignment",
    ("Город", "Место доставки", "Отправитель Город"): "city"
}

DICT_CONTENT_BEFORE_TABLE: Dict[Tuple, str] = {
    ("ДАТА ПРИХОДА", "дата прихода", "Дата прихода", "Дата подхода", "Port of Loading", "Договор с портом "): "date",
    ("ВЫГРУЗКА ГРУЗА С", "Название судна", "Наименование судна", "MANIFEST", "Судно", "Название парохода"):
        "ship_voyage",
    ("[A-Z0-9]",): "ship_voyage_in_other_cells",
    ("Рейс", "Номер рейса"): "voyage",
    ("ПРИЛОЖЕНИЕ", "УВЕДОМЛЕНИЕ О ПРИБЫТИИ"): "ship_voyage_msc"
}