# TeleBot
Бот для рассылки сообщений студентам.
Бот получает список новых сообщений из удаленной базы данных.

## Запуск
Запустить в командной строке в корневой директории команду 
>pip install requirements.txt

 для установки зависимостей.

Для запуска скрипта в командной строке выполнить команду 
>python -m TelegrammBot


## Перед запуском программы
Перед запуском программы необоходимо создать json-файл конфигурации с токеном телеграмм-бота и ссылкой к удаленной БД.
Шаблон файла:
>{
>
  >	"TOKEN":"ТОКЕН_БОТА",
  >	
  > "URL":"URL_ССЫЛКА_НА_УДАЛЕННУЮ_БД"
>	
>}

При запуске скрипта программа попросит указать путь к этому файлу.

## Документация
Для генерации документации по проекту в консоли ввести 
>python setup.py build_shpinx

## Зависимости
| Modules       | Version       |
| ------------- |:-------------:|
|pyTelegramBotAPI | ~4.4.0 |
| setuptools | ~61.2.0 |
| sphinx     | ~4.5.0  |
