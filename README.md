### Описание

Проект представляет собой сервис, который обходит произвольный сайт с глубиной до 2 и сохраняет `html`, `url` и `title` страницы в хранилище.

## Запуск проекта

Для запуска проекта необходимо склонировать проект

```bash
$ git clone https://github.com/EvgeniyAnistratov/site_parser.git
```

Создать файл переменных окружения

```bash
$ cp .env.example .env
```

Настроить переменные окружения в файле .env. Файл переменных окружения используется в файле docker-compose.yml и в программе.

### Описание переменных окружения
- DB_NAME - имя базы данных
- DB_USER - имя пользователя postgresql
- DB_PASSWORD - пароль пользователя базы данных (БД)
- DB_HOST - хост, на котором расположена БД. __ВАЖНО!!!__ Если программа будет запускаться в docker контейнере, то хост должен соответствовать имени сервиса БД в файле
docker-compose.yml. Если программ будет запускаться вне контейнера, то переменная должна хранить IP-адрес или доменное имя, на котором расположена БД.
- DB_PORT - порт, который прослушивается БД
- PG_DATA - директория файлов БД в контейнере. По-умолчанию: ___/var/lib/postgresql/data___

Выполнить построение образа и запуск контейнеров с передачей файла переменных окружения следующей командой.

```bash
$ docker-compose --env-file .env up -d
```

Выполнить команду

```bash
$ docker exec -it python_site_parser /bin/sh
```

Запустить загрузку данных веб-сайта по url и глубине командой

```bash
$ python main.py load <url> --depth=<глубина>
```

Для получения загруженных данных с ограничением количества возращаемых строк из БД необходимо выполнить команду

```bash
$ python main.py get <url> --rows=<кол-во записей>
```

Выйти из docker контейнера командой

```bash
$ exit
```

### Вся последовательность команд

```bash
$ git clone https://github.com/EvgeniyAnistratov/site_parser.git
$ cp .env.example .env
$ docker-compose --env-file .env up -d
$ docker exec -it python_site_parser /bin/sh
$ python main.py load <url> --depth=<глубина>
$ python main.py get <url> --rows=<кол-во записей>
$ exit
```

## Пример работы с программой

___Примечание:___ если при загрузке данных программа обнаружит, что переданные url уже существует в БД, то программа предложит удалить записи из БД и выплонить поиск заново, либо завершить выполнение программы.

```bash
$ python main.py load http://www.google.com --depth=1
Time and memory usage by 'run_with_profile' function.
Maximum used memory: 37.954 MB
CPU Execution time: 1.235 seconds.
All Execution time: 9.891 seconds.
$
$ python main.py load http://www.google.com --depth=1
Url http://www.google.com was parsed.
Input "Y" to clear the database and continue. Input "N" to exit.
N
$
$ python main.py get http://www.google.com --rows=3
Depth: 0: http://www.google.com: Google
Depth: 1: http://maps.google.ru/maps?hl=ru&tab=wl:  Google Карты 
Depth: 1: http://www.google.ru/imghp?hl=ru&tab=wi: Картинки Google
$
```
