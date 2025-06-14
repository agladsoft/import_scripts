import os
import sys
import types
import importlib.util

# Функция для проверки, что модуль можно импортировать
def can_import(module_name):
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

# Если не можем импортировать scripts, но нужно сохранить импорты из scripts
if not can_import('scripts'):
    # Ищем файлы admiral.py и arkas.py в разных местах
    possible_paths = [
        os.path.dirname(os.path.abspath(__file__)),  # Текущая директория
        '/mnt',                                      # Корневой путь в контейнере
        '/import',                                   # Еще один возможный путь
        os.environ.get('XL_IDP_ROOT', '')            # Из переменной окружения
    ]
    
    # Проверяем каждый путь на наличие файлов
    admiral_path = None
    arkas_path = None
    
    for base_path in possible_paths:
        if not base_path:
            continue
            
        # Проверяем наличие файлов напрямую
        if os.path.exists(os.path.join(base_path, 'admiral.py')) and \
           os.path.exists(os.path.join(base_path, 'arkas.py')):
            admiral_path = os.path.join(base_path, 'admiral.py')
            arkas_path = os.path.join(base_path, 'arkas.py')
            break
            
        # Проверяем в подпапке scripts
        if os.path.exists(os.path.join(base_path, 'scripts', 'admiral.py')) and \
           os.path.exists(os.path.join(base_path, 'scripts', 'arkas.py')):
            admiral_path = os.path.join(base_path, 'scripts', 'admiral.py')
            arkas_path = os.path.join(base_path, 'scripts', 'arkas.py')
            break
    
    # Если нашли файлы, создаем виртуальный модуль scripts
    if admiral_path and arkas_path:
        # Создаем модуль scripts
        scripts_module = types.ModuleType('scripts')
        sys.modules['scripts'] = scripts_module
        
        # Загружаем модуль admiral
        spec_admiral = importlib.util.spec_from_file_location('scripts.admiral', admiral_path)
        admiral_module = importlib.util.module_from_spec(spec_admiral)
        sys.modules['scripts.admiral'] = admiral_module
        spec_admiral.loader.exec_module(admiral_module)
        
        # Загружаем модуль arkas
        spec_arkas = importlib.util.spec_from_file_location('scripts.arkas', arkas_path)
        arkas_module = importlib.util.module_from_spec(spec_arkas)
        sys.modules['scripts.arkas'] = arkas_module
        spec_arkas.loader.exec_module(arkas_module)
        
        print(f"Создан виртуальный модуль scripts с admiral.py из {admiral_path} и arkas.py из {arkas_path}", file=sys.stderr)

# Стандартный импорт - теперь должен работать
from scripts.admiral import Admiral, telegram
from scripts.arkas import Arkas


class MLineAdmiral(Admiral):
    """
    MLine наследуется от Admiral с переопределением метода add_frequently_changing_keys.
    """

    def parse_ship_and_voyage(self, parsing_row: str, row: list, column: str, context: dict, key: str) -> None:
        """
        Parsing ship name and voyage in the cells before the table.
        """
        self.logger_write.info(f"Will parse ship and trip in value '{parsing_row}'...")
        ship_and_voyage_list: list = parsing_row.replace(column, "").strip().rsplit(' ', 1)
        context["ship_name"] = ' '.join(ship_and_voyage_list).strip()
        context["voyage"] = 'нет данных'
        self.logger_write.info(f"context now is {context}")


class MLineArkas(Arkas):
    """
    Подкласс Arkas с переопределенным методом add_frequently_changing_keys.
    """

    def add_frequently_changing_keys(self, row: list, parsed_record: dict) -> None:
        """
        Entry in the dictionary of those keys that are often subject to change.
        """
        parsed_record['container_size'] = int(float(row[self.dict_columns_position["container_size"]].strip()))
        parsed_record['container_type'] = row[self.dict_columns_position["container_type"]].strip()
        parsed_record['city'] = row[self.dict_columns_position["city"]]
        parsed_record["tracking_country"] = row[self.dict_columns_position["tracking_country"]].strip()


if __name__ == '__main__':
    input_file = os.path.abspath(sys.argv[1])
    output_folder = sys.argv[2]

    try:
        parsed_data = MLineAdmiral(input_file, output_folder, __file__)
        print(parsed_data.main(is_reversed=True))
        del parsed_data

    except SystemExit as e:
        if e.code in [2, 3]:
            try:
                arkas_parser = MLineArkas(input_file, output_folder, __file__)
                result = arkas_parser.main(is_need_duplicate_containers=False)
                print(result)
                sys.exit(0)

            except Exception as arkas_ex:
                print("6", file=sys.stderr)
                telegram(f'Ошибка {arkas_ex} при обработке через Arkas')
                sys.exit(6)
        else:
            sys.exit(e.code)

    except Exception as ex:
        print("6", file=sys.stderr)
        telegram(f'Ошибка {ex} при обработке файла {input_file}')
        sys.exit(6)