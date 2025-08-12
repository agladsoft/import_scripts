# 🚢 Import Scripts

## 📝 Описание проекта

Данный репозиторий содержит набор скриптов для обработки импортных данных морских терминалов NUTEP и NLE с поддержкой множества судоходных линий. Основной функционал включает в себя:

- 🚛 Парсинг файлов более 40 различных судоходных линий
- 📊 Обработка Excel/CSV файлов с данными импортных грузоперевозок
- 🔄 Стандартизация и унификация данных различных линий
- 🌍 Автоматическое определение портов отправления через микросервисы
- 💾 Сохранение обработанных данных в JSON формате
- 📦 Интеграция с ClickHouse для получения справочных данных
- 📱 Уведомления в Telegram о статусе обработки
- 🔍 Детальное логирование для каждой линии

## 🗂️ Структура проекта

```
import_scripts/
├── Dockerfile                          # Контейнеризация приложения
├── requirements.txt                     # Python зависимости
├── venv/                               # Виртуальное окружение Python
├── bash_dir/                           # Bash скрипты для автоматизации
│   ├── _nutep_lines.sh                # Скрипт запуска для терминала NUTEP
│   ├── _nle_lines.sh                  # Скрипт запуска для терминала NLE
│   ├── _all_lines.sh                  # Запуск всех судоходных линий
│   ├── flat_import_nutep.sh           # Обработчик плоских файлов NUTEP
│   ├── flat_import_nle.sh             # Обработчик плоских файлов NLE
│   └── line_*.sh                      # Скрипты для каждой судоходной линии
├── scripts/                           # Python модули
│   ├── BaseLine.py                    # Базовый класс для всех линий
│   ├── __init__.py                    # Общие функции и константы
│   ├── database.py                    # Интеграция с базой данных
│   ├── parsed.py                      # Модуль обогащения данных портами
│   ├── flat_import_*.py               # Парсеры плоских файлов
│   ├── convert_*.py                   # Утилиты конвертации
│   └── *.py                          # Парсеры для каждой судоходной линии
└── logging/                           # Логи обработки
    └── *.log                         # Файлы логов для каждой линии
```

## ⚙️ Основные компоненты

### 🚛 Поддерживаемые судоходные линии (40+)
- **Admiral** - Admiral Line
- **Akkon Lines** - Akkon Shipping Lines
- **ARKAS** - ARKAS Line
- **Boat Link** - Boat Link Shipping
- **C-STAR** - C-STAR Line
- **CMA CGM** - CMA CGM Group
- **COSCO** - COSCO Shipping Lines
- **ECCL** - Eastern Car Carriers Line
- **Economou** - Economou Lines
- **Econship** - Econship Line
- **Evergreen** - Evergreen Line
- **FESCO** - Far Eastern Shipping Company
- **LAM** - Latin American Maritime
- **Lancer** - Lancer Container Lines
- **Lider Line** - Lider Container Line
- **Login** - Login Line
- **M-Line** - M-Line Shipping
- **Maersk** - A.P. Moller-Maersk
- **Major** - Major Shipping Group
- **Major Cargo Service** - Major Cargo Service Line
- **MAS** - Maritime Agency Services
- **Medkon** - Medkon Lines
- **Milaha** - Qatar Navigation (Milaha)
- **Mohill** - Mohill Shipping
- **MSC** - Mediterranean Shipping Company
- **ONE** - Ocean Network Express
- **OOCL** - Orient Overseas Container Line
- **OVP** - OVP Shipping
- **PJSC Transcontainer** - Transcontainer
- **RC Line** - RC Container Lines
- **Reel Shipping** - Reel Shipping Company
- **Safetrans** - Safetrans Line
- **Sidra** - Sidra Line
- **Silmar** - Silmar Line
- **SINOKOR** - SINOKOR Merchant Marine
- **Smart** - Smart Line
- **UCAK Line** - UCAK Container Line
- **United** - United Line
- **Verim** - Verim Line
- **Verim UNETI** - Verim UNETI Line
- **VUXX Shipping** - VUXX Shipping Line
- **Xinhelu** - Xinhelu Line
- **Yang Ming** - Yang Ming Marine Transport
- **ZIM** - ZIM Integrated Shipping Services

### 🐍 Python модули обработки данных
- **BaseLine.py** - базовый класс с общей логикой парсинга для всех линий
- **flat_import_nutep.py** / **flat_import_nle.py** - парсеры плоских файлов терминалов (где столбцы идут на 1 строке, а дальше уже данные)
- **Специализированные парсеры** - для каждой судоходной линии (40+ файлов)
- **parsed.py** - модуль для автоматического определения портов и обогащения данных
- **database.py** - интеграция с ClickHouse
- **convert_*.py** - утилиты конвертации форматов

### 🔧 Bash скрипты автоматизации
- **_nutep_lines.sh** / **_nle_lines.sh** - главные скрипты для каждого терминала
- **_all_lines.sh** - последовательный запуск всех судоходных линий
- **line_*.sh** - индивидуальные скрипты для каждой линии (40+ файлов)
- **flat_import_*.sh** - обработка плоских импортных файлов

## 🚀 Функциональность

### 🏢 Обработка импортных данных терминалов

#### 🚛 Многолинейная обработка
1. **📄 Парсинг файлов различных форматов**:
   - Excel файлы (.xlsx, .xls)
   - CSV файлы
   - XML файлы
   - Автоматическая конвертация форматов
2. **🔄 Стандартизация данных по линиям**:
   - Унифицированная структура для всех линий
   - Специализированная логика для каждой линии
   - Обработка различных форматов дат и чисел
   - Извлечение судна и рейса из заголовков файлов
3. **🌍 Автоматическое определение портов**:
   - 🔍 Запросы к микросервису определения портов
   - 📦 Определение по номеру контейнера или коносаменту
   - 🚛 Учет специфики различных линий перевозок
   - ⚡ Кеширование результатов для оптимизации

#### 📦 Плоские файлы (flat_import)
1. **📊 Унифицированная обработка терминальных данных**:
   - Стандартизированная структура данных
   - Обработка массовых загрузок
   - Быстрая обработка больших объемов данных
2. **🔄 Разделение по терминалам**:
   - NUTEP - полная функциональность
   - NLE - специализированная обработка

### 🏭 Терминальная специализация

#### 🏢 NUTEP Terminal (порт 8085)
- 🚛 Обработка всех судоходных линий (40+)
- 📦 Обработка плоских импортных файлов
- 🔄 Полный цикл обработки: линии → плоские файлы

#### 🏢 NLE Terminal (порт 8086)
- 🚛 Обработка всех судоходных линий (40+)
- 📦 Обработка плоских импортных файлов
- 🔄 Полный цикл обработки: линии → плоские файлы

### 👁️ Система мониторинга
- 🔍 Автоматическое обнаружение новых файлов для каждой линии
- ⏱️ Обработка файлов не новее 3 секунд для стабильности
- 📝 Детальное логирование процесса обработки каждой линии
- ⚠️ Система кодов ошибок (1-6) с подробным описанием
- 📱 Telegram уведомления о критических ошибках
- 📊 Индивидуальные логи для каждой судоходной линии

## 🔧 Переменные окружения

Для работы системы необходимо настроить следующие переменные окружения:

```bash
# ClickHouse подключение
HOST=clickhouse_host
DATABASE=database_name
USERNAME_DB=username
PASSWORD=password

# Микросервис определения портов
IP_ADDRESS_CONSIGNMENTS=service_ip
PORT=service_port

# Пути к данным
XL_IDP_ROOT=/path/to/import/data
XL_IDP_PATH_IMPORT=/path/to/import/files

# Терминал (nutep или nle)
XL_IMPORT_TERMINAL=nutep_or_nle

# Telegram уведомления
TOKEN_TELEGRAM=your_bot_token
CHAT_ID=your_chat_id
TOPIC=your_topic
ID=your_message_id

# Docker пути
XL_IDP_PATH_DOCKER=/app/scripts
```

## 🛠️ Сборка и запуск

### 💻 Локальная разработка

1. **📋 Клонирование репозитория:**
```bash
git clone <repository_url>
cd import_scripts
```

2. **🌐 Создание виртуального окружения:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **📦 Установка зависимостей:**
```bash
pip install -r requirements.txt
```

4. **⚙️ Настройка переменных окружения:**
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

5. **🚀 Запуск обработки:**
```bash
# Разовая обработка файла конкретной линии
python3 scripts/msc.py /path/to/file.csv /path/to/output/

# Разовая обработка плоского файла
python3 scripts/flat_import_nutep.py /path/to/file.xlsx /path/to/output/

# Запуск мониторинга для NUTEP (все линии + плоские файлы)
export XL_IMPORT_TERMINAL=nutep
bash bash_dir/_nutep_lines.sh

# Запуск мониторинга для NLE (все линии + плоские файлы)
export XL_IMPORT_TERMINAL=nle
bash bash_dir/_nle_lines.sh

# Запуск только конкретной линии
bash bash_dir/line_msc.sh
```

### 🐳 Docker Compose (рекомендуемый способ)

Проект является частью большой экосистемы микросервисов и запускается через общий docker-compose файл для двух терминалов:

#### 🏢 Контейнер NUTEP (порт 8085)
```yaml
import_nutep:
  container_name: import_nutep
  restart: always
  ports:
    - "8085:8085"
  volumes:
    - ${XL_IDP_PATH}:${XL_IDP_PATH_DOCKER}
    - ${XL_IDP_ROOT}:${XL_IDP_PATH_IMPORT}
  environment:
    XL_IDP_ROOT: ${XL_IDP_PATH_DOCKER}
    XL_IDP_PATH_IMPORT: ${XL_IDP_PATH_IMPORT}
    IP_ADDRESS_CONSIGNMENTS: ${IP_ADDRESS_CONSIGNMENTS}
    XL_IMPORT_TERMINAL: nutep
    TOKEN_TELEGRAM: ${TOKEN_TELEGRAM}
  build:
    context: import
    dockerfile: ./Dockerfile
    args:
      XL_IDP_PATH_DOCKER: ${XL_IDP_PATH_DOCKER}
  command: bash -c "sh ${XL_IDP_PATH_DOCKER}/bash_dir/_nutep_lines.sh"
  networks:
    - postgres
```

#### 🏢 Контейнер NLE (порт 8086)
```yaml
import_nle:
  container_name: import_nle
  restart: always
  ports:
    - "8086:8086"
  volumes:
    - ${XL_IDP_PATH}:${XL_IDP_PATH_DOCKER}
    - ${XL_IDP_ROOT}:${XL_IDP_PATH_IMPORT}
  environment:
    XL_IDP_ROOT: ${XL_IDP_PATH_DOCKER}
    XL_IDP_PATH_IMPORT: ${XL_IDP_PATH_IMPORT}
    IP_ADDRESS_CONSIGNMENTS: ${IP_ADDRESS_CONSIGNMENTS}
    XL_IMPORT_TERMINAL: nle
    TOKEN_TELEGRAM: ${TOKEN_TELEGRAM}
  build:
    context: import
    dockerfile: ./Dockerfile
    args:
      XL_IDP_PATH_DOCKER: ${XL_IDP_PATH_DOCKER}
  command: bash -c "sh ${XL_IDP_PATH_DOCKER}/bash_dir/_nle_lines.sh"
  networks:
    - postgres
```

**📋 Необходимые переменные окружения в .env:**
```bash
# Пути к скриптам и данным
XL_IDP_PATH=/path/to/import_scripts
XL_IDP_ROOT=/path/to/import/data
XL_IDP_PATH_DOCKER=/app/scripts
XL_IDP_PATH_IMPORT=/app/data

# Микросервис определения портов
IP_ADDRESS_CONSIGNMENTS=service_ip
PORT=service_port

# Telegram уведомления
TOKEN_TELEGRAM=your_bot_token
CHAT_ID=your_chat_id
TOPIC=your_topic
ID=your_message_id

# ClickHouse подключение (используется через переменные окружения)
HOST=clickhouse_host
DATABASE=database_name
USERNAME_DB=username
PASSWORD=password
```

**🚀 Запуск:**
```bash
# Запуск терминала NUTEP
docker-compose up -d import_nutep

# Запуск терминала NLE
docker-compose up -d import_nle

# Запуск обоих терминалов
docker-compose up -d import_nutep import_nle
```

### 📋 Системные требования

- **Python**: 3.8+
- **ОС**: Linux (предпочтительно), Windows, macOS
- **Память**: минимум 4GB RAM (для обработки 40+ линий)
- **Диск**: зависит от объема обрабатываемых данных
- **Сеть**: доступ к ClickHouse и микросервису определения портов

## 📊 Структура данных

### 📥 Входные данные

#### 🚛 Файлы судоходных линий
Каждая линия имеет специфический формат, но общие поля включают:
- **Логистические данные**: Дата отгрузки, Судно, Рейс
- **Контейнерные данные**: Номер контейнера, Размер, Тип, Количество
- **Грузовые данные**: Наименование товара, Вес, ТНВЭД
- **Участники**: Отправитель, Получатель, Агент
- **География**: Порт отправления, Порт назначения
- **Документооборот**: Коносамент, номера документов

#### 📦 Плоские файлы терминалов
- Унифицированная структура данных
- Массовые загрузки импортных данных
- Стандартизированные поля для всех терминалов

### 📤 Выходные данные
- **JSON файлы** - стандартизированные данные с англоязычными полями
- **Обогащенные данные**:
  - 🌍 Автоматически определенные порты отправления
  - 🚛 Унифицированные названия линий
  - 📊 Флаги успешности автоматического трекинга
  - 🕒 Метаданные обработки файлов
  - 📍 Географическая привязка

## 📋 Структура обрабатываемых папок

### 🚛 Структура по линиям (для каждого терминала)
```
lines_nutep/ или lines_nle/
├── admiral_tracking/           # Admiral Line
├── arkas_tracking/            # ARKAS Line
├── cma_cgm_tracking/          # CMA CGM
├── cosco_tracking/            # COSCO Shipping
├── evergreen_tracking/        # Evergreen Line
├── fesco_tracking/            # FESCO
├── maersk_tracking/           # Maersk Line
├── msc_tracking/              # MSC
├── one_tracking/              # ONE Line
├── sinokor_tracking/          # SINOKOR
└── ... (30+ других линий)
```

### 📦 Плоские файлы
```
lines_nutep/ или lines_nle/
├── flat_import_nutep_tracking/        # Основные плоские файлы NUTEP
├── flat_import_nutep_tracking_update/ # Обновления плоских файлов NUTEP
├── flat_import_nle_tracking/          # Основные плоские файлы NLE
└── flat_import_nle_tracking_update/   # Обновления плоских файлов NLE
```

Каждая папка содержит:
- **csv/** - конвертированные CSV файлы (для линий)
- **done/** - успешно обработанные файлы  
- **json/** - результаты обработки в JSON формате
- **error_*** - файлы с ошибками обработки

## 🔍 Система кодов ошибок

Система использует детализированные коды ошибок для диагностики:

- **Код 1** - Ошибка в названии файла (отсутствие даты)
- **Код 2** - Изменение структуры колонок или отсутствие столбца
- **Код 3** - Отсутствие даты, рейса или названия судна в заголовке
- **Код 4** - Образование пустого JSON файла
- **Код 5** - Ошибка обработки данных внутри таблицы
- **Код 6** - Неизвестная ошибка обработки скриптов

## 🔍 Мониторинг и отладка

### 📜 Логи
- **Индивидуальные логи** для каждой судоходной линии
- Подключение к ClickHouse
- Процесс запросов к микросервису определения портов
- Статус обработки каждого файла
- Детальная информация об ошибках с кодами

### 📱 Telegram уведомления
- Критические ошибки обработки файлов
- Проблемы с подключением к внешним сервисам
- Статистика обработки по линиям

### ⚠️ Обработка ошибок
- Проблемные файлы перемещаются с префиксом "error_code_N_"
- Автоматическая конвертация форматов Excel → CSV → JSON
- Повторные попытки обработки проблемных файлов
- Специализированная обработка ошибок для каждой линии

## 🧪 Разработка и тестирование

### ➕ Добавление новой судоходной линии
1. Создайте новый Python модуль в папке `scripts/` (например, `new_line.py`)
2. Наследуйте от класса `BaseLine` и реализуйте специфическую логику
3. Создайте соответствующий bash скрипт `bash_dir/line_new_line.sh`
4. Добавьте вызов скрипта в `_all_lines.sh`
5. Создайте структуру папок для новой линии

### 🧪 Тестирование
```bash
# Тестирование конкретной линии
python3 scripts/msc.py test_file.csv output/

# Тестирование плоского файла
python3 scripts/flat_import_nutep.py test_file.xlsx output/

# Тестирование конкретной линии через bash
bash bash_dir/line_msc.sh

# Проверка подключения к ClickHouse
python3 -c "from scripts.database import clickhouse_client; clickhouse_client()"

# Тестирование определения портов
python3 -c "from scripts.parsed import ParsedDf; import pandas as pd; df = pd.DataFrame([{'line': 'MSC', 'container_number': 'TEST123', 'direction': 'import'}]); ParsedDf(df).get_port()"
```

### 🔧 Отладка конкретной линии
```bash
# Включение детального логирования
export XL_IMPORT_TERMINAL=nutep
bash bash_dir/line_msc.sh

# Проверка логов конкретной линии
tail -f logging/msc.log

# Проверка файлов с ошибками
ls lines_nutep/msc_tracking/error_*
```

## 🆘 Техническая поддержка

При возникновении проблем:
1. 📋 Проверьте логи конкретной линии в папке `logging/`
2. 🔍 Изучите коды ошибок в файлах error_code_N_*
3. ✅ Убедитесь в доступности ClickHouse
4. 🌐 Проверьте подключение к микросервису определения портов
5. 📁 Проверьте права доступа к папкам с данными для каждого терминала
6. 📊 Убедитесь в корректности структуры файлов для каждой линии
7. 🚛 Проверьте настройки переменной XL_IMPORT_TERMINAL
8. 🔄 Проверьте статус обработки файлов (done/, csv/, json/, error_*)

## 🎯 Особенности архитектуры

### 🏗️ Масштабируемость
- Модульная архитектура с базовым классом `BaseLine`
- Независимая обработка каждой судоходной линии
- Параллельная работа двух терминалов
- Легкое добавление новых линий

### 🔄 Надежность
- Система кодов ошибок для быстрой диагностики
- Автоматическое перемещение проблемных файлов
- Детальное логирование каждого этапа обработки
- Telegram уведомления о критических сбоях

### ⚡ Производительность
- Кеширование результатов запросов к внешним сервисам
- Оптимизированная конвертация форматов файлов
- Батчевая обработка файлов
- Эффективная работа с базой данных ClickHouse

## 📄 Лицензия

Проект предназначен для внутреннего использования.