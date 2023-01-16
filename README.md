# Тестовое задание для python-разработчика

![Project language][badge_language]
![Docker][badge_docker]
[![Build Status][badge_build]][link_build]
[![Do something awesome][badge_use_template]][use_this_repo_template]

### Описание

Реализовать сервис, который обходит произвольный сайт с глубиной до 2 и сохраняет `html`, `url` и `title` страницы в хранилище.

Примеры сайтов:

* `https://ria.ru`
* `http://www.vesti.ru`
* `http://echo.msk.ru`
* `http://tass.ru/ural` 
* `https://lenta.ru`
* и любой другой, на котором есть ссылки
    
Оптимизировать прогрузку по потреблению памяти и по времени. 
Замерить время выполнения и потребление памяти загрузки.

> При depth=0 необходимо сохранить html, title, url исходного веб-сайта.
>
> На каждом depth=i+1 качаем страницы ссылок с i страницы (то есть глубина 2 это - главная, ссылки на главной и ссылки на страницах ссылок с главной).

### CLI

* По урлу сайта и глубине обхода загружаются данные.
* По урлу сайта из хранилища можно получить `n` прогруженных страниц (`url` и `title`).
    
Пример:

```
spider.py load http://www.vesti.ru/ --depth 2
>> ok, execution time: 10s, peak memory usage: 100 Mb
spider.py get http://www.vesti.ru/ -n 2
>> http://www.vesti.ru/news/: "Вести.Ru: новости, видео и фото дня"
>> http://www.vestifinance.ru/: "Вести Экономика: Главные события российской и мировой экономики, деловые новости,  фондовый рынок"
```

### Требования

* Язык реализации `python3.6+`
* Выбор хранилища произвольный (`PostgreSQL`/`Redis`/`ElasticSearch` и любой другой на ваш выбор) 
* Стек технологий произвольный
* Выбор библиотек произвольный
* Решение оформить как проект на любом git-сервисе
* Описать в `README.md` установку, запуск, python и другие зависимости для запуска

### Было бы большим плюсом

* Docker multistage build
* Run Docker as a non-root user  
* Написать тесты при помощи `pytest`/`unittest` и любой другой на ваш выбор
    
## Как начать выполнение тестового задания?

Для выполнения задания лучше всего использовать данный репозиторий как шаблон, для чего просто перейдите по [**этой ссылке**][use_this_repo_template].

Данный репозиторий уже содержит `Dockerfile`, `docker-compose.yml` и `Makefile` для быстрого запуска приложения силами `docker` _(нет необходимости устанавливать python и пр. локально)_. Всё, что необходимо - это установленные локально `docker` и `docker-compose`. После клонирования репозитория просто выполните `docker-compose up -d` и/или натравите PyCharm на `docker-compose` - и можно приступать к написанию полезного кода.

## Результат выполнения

* Ссылку на репозиторий с вашей реализацией необходимо отправить нашему HR или TeamLead, от которого вы получили ссылку на данный репозиторий.

* Приложение должно успешно запускаться после выполнения:

```bash
$ git clone ...
$ make build
$ docker-compose up -d
$ docker-compose run --rm app ./app
```

* Проходить _все_ тесты (при их наличии).

> Если для запуска приожения потребуется другой набор команд - обязательно отразите это в файле `README.md` вашего репозитория.

> Если в процессе выполнения у вас возникнут какие-либо неразрешимые вопросы - создайте [соответствующий issue][link_create_issue] в данном репозитории. На вопросы касательно деталей реализации ("А лучше так и так?") - вероятнее всего вы получите ответ "Как вы посчитаете правильнее".

[badge_build]:https://github.com/avtocod/python-developer-test-task/workflows/CI/badge.svg
[badge_language]:https://img.shields.io/badge/python-3-yellow?longCache=true
[badge_docker]:https://img.shields.io/badge/docker-enable-blue?longCache=true
[badge_use_template]:https://img.shields.io/badge/start-this_template_using-success.svg?longCache=true
[link_build]:https://github.com/avtocod/python-developer-test-task/actions
[link_create_issue]:https://github.com/avtocod/python-developer-test-task/issues/new
[use_this_repo_template]:https://github.com/avtocod/python-developer-test-task/generate
