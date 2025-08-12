# 🏗️ Архитектура обработки судоходных линий

## 📝 Обзор архитектуры

Система обработки данных судоходных линий построена на основе объектно-ориентированного подхода с использованием базового класса `BaseLine` и специализированных наследников для каждой линии. Архитектура обеспечивает единообразную обработку различных форматов данных от 40+ судоходных компаний.

## 🏛️ Основные принципы архитектуры

### 🧱 Наследование и полиморфизм
- **Базовый класс `BaseLine`** содержит общую логику обработки
- **Специализированные классы** (например, `Admiral`) наследуют базовую функциональность
- **Переопределение методов** для специфических требований каждой линии

### 🔄 Единый алгоритм обработки
1. **Предобработка файла** - удаление пустых строк и колонок
2. **Извлечение метаданных** - дата, судно, рейс из заголовков
3. **Определение структуры** - поиск и анализ заголовков таблиц
4. **Парсинг данных** - извлечение данных из строк таблицы
5. **Обогащение данных** - определение портов через внешние API
6. **Постобработка** - унификация и очистка данных
7. **Сохранение результата** - экспорт в JSON формат

## 📁 Структура классов

### 🏗️ BaseLine - Базовый класс

```python
class BaseLine:
    """
    Базовый класс для всех судоходных линий
    Содержит общую логику обработки файлов
    """
    
    def __init__(self, input_file_path: str, output_folder: str, line_file: str):
        # Инициализация путей и логгера
        
    # Основные методы обработки:
    def main() -> int                              # Главный метод обработки
    def remove_empty_columns_and_rows() -> str     # Очистка пустых данных
    def create_parsed_data_and_context() -> tuple  # Создание контекста
    def check_errors_in_header()                   # Валидация заголовков
    def parse_row()                               # Парсинг строки данных
    def write_data_in_file()                      # Сохранение в JSON
    
    # Вспомогательные методы:
    def is_digit() -> bool                        # Проверка числового значения
    def merge_two_dicts() -> dict                 # Слияние словарей
    def remove_symbols_in_columns() -> str        # Очистка заголовков
    def fill_data_with_duplicate_containers()     # Заполнение дублированных контейнеров
```

### 🚢 Admiral - Пример специализированного класса

```python
class Admiral(Singleton, BaseLine):
    """
    Специализированный класс для линии Admiral
    Наследует базовую функциональность и добавляет специфическую логику
    """
    
    # Определение структуры колонок для данной линии
    dict_columns_position: Dict[str, Union[None, int]] = {
        "number_pp": None,
        "container_size_and_type": None,
        "container_number": None,
        "container_seal": None,
        "goods_weight_with_package": None,
        "package_number": None,
        "goods_name": None,
        "shipper_name": None,
        "tracking_country": None,
        "consignee_name": None,
        "consignment": None,
        "city": None
    }
    
    # Переопределенные методы для специфической логики:
    def parse_date()                              # Парсинг даты в формате Admiral
    def parse_content_before_table()              # Извлечение метаданных
    def parse_ship_and_voyage()                   # Парсинг судна и рейса
    def get_columns_position()                    # Определение позиций колонок
    def add_frequently_changing_keys()            # Обработка изменяемых полей
    def is_table_starting() -> bool               # Определение начала таблицы
```

## 🔄 Алгоритм обработки файла

### 1️⃣ Предобработка данных

```python
def main(self):
    # 1. Удаление пустых строк и колонок
    file_name_save = self.remove_empty_columns_and_rows()
    
    # 2. Основная обработка
    list_data = self.__get_content_from_file(file_name_save, coefficient_of_header)
    
    # 3. Заполнение дублированных контейнеров
    if is_need_duplicate_containers:
        list_data = self.fill_data_with_duplicate_containers(list_data, sign)
```

### 2️⃣ Создание контекста обработки

```python
def create_parsed_data_and_context(self, file_name_save, input_file_path):
    # Извлечение даты из имени файла
    date_previous = re.match(r'\d{2,4}.\d{1,2}', os.path.basename(file_name_save))
    
    # Создание контекста с метаданными
    context = dict(
        line=self.line_file,
        terminal="НУТЭП" if os.environ.get('XL_IMPORT_TERMINAL') == "nutep" else "НЛЭ",
        parsed_on=str(datetime.strptime(date_previous, "%Y.%m.%d").date())
    )
    
    # Чтение CSV данных
    with open(file_name_save, newline='') as csvfile:
        rows = list(csv.reader(csvfile))
    
    return rows, context
```

### 3️⃣ Обработка каждой строки

```python
def process_row(self, row, rows, index, list_data, context, list_columns, coefficient_of_header):
    # Определение типа строки
    if self.get_probability_of_header(row, list_columns) > coefficient_of_header:
        # Обработка заголовка таблицы
        self.check_errors_in_header(row, context)
        
    elif self.is_table_starting(row):
        # Обработка строки данных
        self.get_content_in_table(row, rows, index, list_data, context)
        
    else:
        # Извлечение метаданных (дата, судно, рейс)
        self.get_content_before_table(row, context, LIST_MONTH)
```

### 4️⃣ Парсинг строки данных

```python
def parse_row(self, index, row, rows, context, list_data):
    parsed_record = {}
    
    # Обработка специфических полей для данной линии
    self.add_frequently_changing_keys(row, parsed_record)
    
    # Извлечение стандартных полей
    record = self.add_value_from_data_to_list(
        row, 
        self.dict_columns_position["container_number"],
        self.dict_columns_position["goods_weight_with_package"],
        self.dict_columns_position["package_number"],
        # ... другие поля
        parsed_record,
        context
    )
    
    list_data.append(record)
```

### 5️⃣ Обогащение данных портами

```python
def get_seaport_from_website(self, list_data):
    if self.line_file in LIST_LINES:
        # Инициализация сервиса определения портов
        seaport_empty_containers = SeaportEmptyContainers(self.logger_write)
        
        # Обогащение данных через внешние API
        list_data = self.parsed_line(list_data)
        
        # Специальная обработка для пустых контейнеров
        self.get_seaport_from_shipper(seaport_empty_containers, list_data)
```

## 🎛️ Система конфигурации

### 📋 Словари конфигурации (в `__init__.py`)

```python
# Соответствие русских заголовков английским полям
DICT_HEADERS_COLUMN_ENG = {
    ("№ п/п", "No", "N п/п"): "number_pp",
    ("Размер и тип контейнера", "Размер/тип контейнера"): "container_size_and_type",
    ("Номер контейнера", "№ контейнера"): "container_number",
    ("Пломба", "№ пломбы"): "container_seal",
    # ... другие соответствия
}

# Извлечение метаданных из заголовков файлов
DICT_CONTENT_BEFORE_TABLE = {
    ("Дата прихода:", "Дата:"): "shipment_date",
    ("Судно:", "Название судна:"): "ship_voyage",
    ("Рейс:", "Номер рейса:"): "ship_voyage",
}

# Список месяцев для парсинга дат
LIST_MONTH = [
    "январь", "февраль", "март", "апрель",
    "май", "июнь", "июль", "август",
    "сентябрь", "октябрь", "ноябрь", "декабрь"
]
```

### 🔧 Параметры обработки для каждой линии

```python
# Пример вызова с настройками для конкретной линии
admiral = Admiral(input_file, output_folder, __file__)
result = admiral.main(
    is_need_duplicate_containers=True,  # Заполнять дублированные контейнеры
    is_reversed=True,                   # Обратный порядок обработки
    sign='',                           # Символ дублирования
    coefficient_of_header=30           # Порог определения заголовка (%)
)
```

## 🔍 Система обработки ошибок

### 📊 Коды ошибок

```python
data_error = {
    '1': 'Ошибка отсутствия даты в названии файла',
    '2': 'Изменение названия колонок или отсутствие столбца',
    '3': 'Отсутствие даты, рейса или названия судна в заголовке',
    '4': 'Образование пустого JSON файла',
    '5': 'Ошибка обработки данных внутри таблицы',
    '6': 'Неизвестная ошибка обработки скриптов'
}
```

### ⚠️ Обработка исключений

```python
def get_content_in_table(self, row, rows, index, list_data, context):
    try:
        self.parse_row(index, row, rows, context, list_data)
    except (IndexError, ValueError, TypeError) as ex:
        # Логирование ошибки
        self.logger_write.error(f"Error code 5: error processing in row {index + 1}!")
        
        # Уведомление в Telegram
        telegram(f'Ошибка возникла в строке {index + 1} Файла {self.input_file_path}.')
        
        # Завершение с кодом ошибки
        print(f"5_in_row_{index + 1}", file=sys.stderr)
        sys.exit(5)
```

## 🚀 Создание новой судоходной линии

### 1️⃣ Создание класса наследника

```python
# scripts/new_line.py
from BaseLine import BaseLine
from __init__ import *

class NewLine(BaseLine):
    # Определение структуры колонок
    dict_columns_position = {
        "container_number": None,
        "goods_name": None,
        # ... другие поля специфичные для этой линии
    }
    
    def parse_date(self, parsing_row, month_list, context, row):
        """Специфический парсинг даты для новой линии"""
        # Реализация парсинга даты
        pass
    
    def add_frequently_changing_keys(self, row, parsed_record):
        """Обработка специфических полей новой линии"""
        # Извлечение и обработка специфических данных
        pass
    
    def is_table_starting(self, row):
        """Определение начала таблицы данных"""
        # Логика определения начала таблицы
        return bool_condition

if __name__ == '__main__':
    parser = NewLine(sys.argv[1], sys.argv[2], __file__)
    try:
        print(parser.main())
    except Exception as ex:
        telegram(f'Ошибка {ex} при обработке файла {parser.input_file_path}.')
        print("6", file=sys.stderr)
        sys.exit(6)
```

### 2️⃣ Создание bash скрипта

```bash
# bash_dir/line_new_line.sh
#!/bin/bash

xls_path="${XL_IDP_PATH_IMPORT}/lines_${XL_IMPORT_TERMINAL}/new_line_tracking"

# Создание необходимых папок
csv_path="${xls_path}"/csv
done_path="${xls_path}"/done
json_path="${xls_path}"/json

mkdir -p "${csv_path}" "${done_path}" "${json_path}"

# Обработка файлов
find "${xls_path}" -maxdepth 1 -type f \( -name "*.xls*" -or -name "*.xml" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do
    if [[ "${file}" == *"error_"* ]]; then
        continue
    fi
    
    mime_type=$(file -b --mime-type "$file")
    
    # Конвертация в CSV
    csv_name="${csv_path}/$(basename "${file}").csv"
    if [[ ${mime_type} = "application/vnd.ms-excel" ]]; then
        in2csv -f xls "${file}" > "${csv_name}"
    elif [[ ${mime_type} = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ]]; then
        in2csv -f xlsx "${file}" > "${csv_name}"
    fi
    
    if [ $? -eq 0 ]; then
        mv "${file}" "${done_path}"
    else
        mv "${file}" "${xls_path}/error_$(basename "${file}")"
        continue
    fi
    
    # Обработка через Python скрипт
    exit_message=$(python3 ${XL_IDP_ROOT}/scripts/new_line.py "${csv_name}" "${json_path}" 2>&1 > /dev/null)
    exit_code=$?
    
    if [[ ${exit_code} == 0 ]]; then
        mv "${csv_name}" "${done_path}"
    else
        mv "${csv_name}" "${xls_path}/error_code_${exit_message}_$(basename "${csv_name}")"
    fi
done
```

### 3️⃣ Добавление в общий список

```bash
# bash_dir/_all_lines.sh
# Добавить строку:
${XL_IDP_ROOT}/bash_dir/line_new_line.sh
```

## 🎯 Особенности архитектуры

### 🏗️ Масштабируемость
- **Модульная структура** - каждая линия в отдельном файле
- **Единый интерфейс** - все классы наследуют от BaseLine
- **Конфигурируемость** - настройки через словари в `__init__.py`
- **Легкое расширение** - добавление новой линии требует минимальных изменений

### 🔄 Гибкость
- **Переопределение методов** - каждая линия может изменить любой аспект обработки
- **Параметризация** - настройка поведения через параметры метода `main()`
- **Условная обработка** - различная логика для разных типов данных

### 🛡️ Надежность
- **Детальная система ошибок** - 6 типов кодов ошибок
- **Логирование на каждом этапе** - отслеживание всех операций
- **Graceful degradation** - обработка частичных ошибок
- **Уведомления в Telegram** - мгновенное оповещение о проблемах

### ⚡ Производительность
- **Потоковая обработка** - построчная обработка больших файлов
- **Кеширование результатов** - избежание повторных API запросов
- **Паттерн Singleton** - один экземпляр парсера для оптимизации памяти
- **Ленивые вычисления** - обработка только необходимых данных

## 📊 Метрики и мониторинг

### 📈 Возвращаемые метрики
```python
def main(self) -> int:
    # Основная обработка
    # ...
    
    # Возврат количества уникальных контейнеров
    return len(self.count_unique_containers(list_data))
```

### 📝 Логирование процесса
```python
# Логирование на каждом этапе
self.logger_write.info(f"Will parse date in value {parsing_row}")
self.logger_write.info(f"context now is {context}")
self.logger_write.info(f"record is {record}")
self.logger_write.info(f"Length is unique containers {len(set_container)}")
```

### 🔔 Система уведомлений
```python
def telegram(message):
    # Отправка уведомлений о критических ошибках
    # Интеграция с Telegram Bot API для мгновенных уведомлений
```

## 🎛️ Конфигурационные параметры

### 🎯 Настройки обработки
- **coefficient_of_header** (30%) - порог определения заголовка таблицы
- **is_need_duplicate_containers** (bool) - заполнение повторяющихся контейнеров
- **is_reversed** (bool) - обратный порядок обработки данных
- **sign** (str) - символ обозначения дублирования контейнера

### 📁 Структура директорий
```
lines_terminal/
├── line_name_tracking/          # Папка для файлов линии
│   ├── csv/                     # Конвертированные CSV файлы
│   ├── done/                    # Успешно обработанные файлы
│   ├── json/                    # Результаты в JSON формате
│   └── error_*                  # Файлы с ошибками
```

Эта архитектура обеспечивает надежную, масштабируемую и легко поддерживаемую систему обработки данных от множества судоходных линий с различными форматами данных.