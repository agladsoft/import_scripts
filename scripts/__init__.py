import os
import requests
from notifiers import get_notifier
from typing import Dict, Tuple, List
from logging import Logger, getLogger, INFO, FileHandler


# XL_IDP_ROOT = '/home/uventus/PycharmProjects/New_Proect/ruscon/docker_project/import_scripts/scripts/None'

def write_log(line_file: str) -> Logger:
    full_dir_name_logging: str = f'{os.environ.get("XL_IDP_ROOT")}/logging'
    # full_dir_name_logging: str = f'{XL_IDP_ROOT}/logging'
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
                         'ДЕКАБРЬ', "Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа",
                         "Сентября",
                         "Октября", "Ноября", "Декабря", "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль",
                         "Август", "Сентябрь",
                         "Октябрь", "Ноябрь", "Декабрь"]

DICT_HEADERS_COLUMN_ENG: Dict[Tuple, str] = {
    ("№ п/п", "№", "№ пп."): "number_pp",
    ("Статус", "Тип", "Type"): "container_size_and_type",
    ("Тип",): "container_type",
    ("Размер",): "container_size",
    ("Номер контейнера", "№контейнера", "№ контейнера", "Container", "Номер Контейнера"): "container_number",
    ("Пломба", "№ пломбы", "№пломбы"): "container_seal",
    ("Вес брутто (кг)", "Вес груза", "Вес груза брт,кг", "Вес груза брт, кг", "Weight",
     "Вес, бр. груза", "Вес, бр. груза, кг"): "goods_weight_with_package",
    ("Количество мест", "Кол-во мест", "мест", "Кол-во", "Кол-во мест", "Places", "К-во мест", "К-во мест/вес товара",
     "Кол-о мест", "Кол -во мест"): "package_number",
    ("Наименование груза", "Наименование заявленного груза", "Наименование заявленного груза (рус)", "Груз"):
        "goods_name",
    ("ТНВЭД", "КОД ТНВЭД", "Код Тн ВЭД", "Российский Код ТНВЭД (10 знаков)", "Код ТНВЭД"): "tnved",
    ("Отправитель", "Грузоотправитель", "Shipper To Order"): "shipper_name",
    ("Страна отправителя", "Страна грузоотправителя", "Страна отправления", "Страна", "Страна порта погрузки",
     "Страна затарки", "Страна погрузки", "Страна грузоотправителя", "Отправитель Страна", "Страна  грузоотправителя"):
        "tracking_country",
    ("Получатель", "Грузополучатель", "Consignee Seal", "Грузополуча тель"): "consignee_name",
    ("Коносамент", "№ к/с", "№ Коносамента", "№коносамента", "Bill of Lading", "№ К/с"): "consignment",
    ("Город", "Место доставки", "Отправитель Город"): "city"
}

DICT_CONTENT_BEFORE_TABLE: Dict[Tuple, str] = {
    ("ДАТА ПРИХОДА", "дата прихода", "Дата прихода", "Дата подхода", "Port of Loading", "Договор с портом ",
     "Дата прибытия"): "shipment_date",
    ("ВЫГРУЗКА ГРУЗА С", "Название судна", "Наименование судна", "MANIFEST", "Судно", "Название парохода"):
        "ship_voyage",
    ("[A-Z0-9]",): "ship_voyage_in_other_cells",
    ("Рейс", "Номер рейса", "рейс"): "voyage",
    ("ПРИЛОЖЕНИЕ", "УВЕДОМЛЕНИЕ О ПРИБЫТИИ"): "ship_voyage_msc"
}


def get_my_env_var(var_name: str) -> str:
    try:
        return os.environ[var_name]
    except KeyError as e:
        raise MissingEnvironmentVariable(f"{var_name} does not exist") from e


class MissingEnvironmentVariable(Exception):
    pass


def telegram(message):
    # teg = get_notifier('telegram')
    chat_id = get_my_env_var('CHAT_ID')
    token = get_my_env_var('TOKEN')
    topic = get_my_env_var('TOPIC')
    message_id = get_my_env_var('ID')
    # teg.notify(token=get_my_env_var('TOKEN'), chat_id=get_my_env_var('CHAT_ID'), message=message)
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {"chat_id": f"{chat_id}/{topic}", "text": message,
              'reply_to_message_id': message_id}  # Добавляем /2 для указания второго подканала
    # response = requests.get(url, params=params)
