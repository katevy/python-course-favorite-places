Любимые места
=============

Сервис для сохранения информации о любимых местах.

Зависимости
===========
Установите требуемое ПО:

1. Docker для контейнеризации – |link_docker|

.. |link_docker| raw:: html

   <a href="https://www.docker.com" target="_blank">Docker Desktop</a>

2. Для работы с системой контроля версий – |link_git|

.. |link_git| raw:: html

   <a href="https://github.com/git-guides/install-git" target="_blank">Git</a>

3. IDE для работы с исходным кодом – |link_pycharm|

.. |link_pycharm| raw:: html

    <a href="https://www.jetbrains.com/ru-ru/pycharm/download" target="_blank">PyCharm</a>


Установка
=========
1. Клонируйте репозиторий проекта в свою рабочую директорию:

    .. code-block:: console
        git clone https://github.com/katevy/python-course-favorite-places.git
Перед началом использования приложения необходимо его сконфигурировать.

.. note::

    Для конфигурации выполните команды, описанные ниже, находясь в корневой директории проекта (на уровне с директорией `src`).

2. Скопируйте файл настроек `.env.sample`, создав файл `.env`:
    .. code-block:: console
        cp .env.sample .env
    Этот файл содержит преднастроенные переменные окружения, значения которых будут общими для всего приложения.
    Файл примера (`.env.sample`) содержит набор переменных со значениями по умолчанию.
    Созданный файл `.env` можно настроить в зависимости от окружения.

    .. warning::

        Никогда не добавляйте в систему контроля версий заполненный файл `.env` для предотвращения компрометации информации о конфигурации приложения.

3. Соберите Docker-контейнер с помощью Docker Compose:
    .. code-block:: console
        docker compose build
    Данную команду необходимо выполнять повторно в случае обновления зависимостей в файле `requirements.txt`.

4. После сборки контейнеров можно их запустить командой:
    .. code-block:: console
        docker compose up
    Данная команда запустит собранные контейнеры для приложения и базы данных.
    Когда запуск завершится, сервер начнет работать по адресу `http://0.0.0.0:8010`.


Работа с базой данных
=============
Для правильной работы приложения необходимо настроить базу данных (создать в ней таблицы).
    Для этого нужно применить миграции внутри контейнера приложения.
    Данная команда позволит зайти в контейнер приложения:

    .. code-block:: console
        docker compose exec favorite-places-app bash
    Для применения миграций выполните команду:

    .. code-block:: console
        alembic upgrade head
    После выполнения команды в базе данных будут созданы все нужные таблицы.


Автоматизация
---------------------
Проект содержит специальный файл (`Makefile`) для автоматизации выполнения команд:

1. Сборка Docker-контейнера.
.. code-block::console
    make build
2. Генерация документации.
.. code-block::console
    make docs-html
3. Запуск форматирования кода.
.. code-block::console
    make format
4. Запуск статического анализа кода (выявление ошибок типов и форматирования кода).
.. code-block::console
    make lint
5. Запуск автоматических тестов.
.. code-block::console
    make test
6. Запуск всех функций поддержки качества кода (форматирование, линтеры, автотесты).
.. code-block::console
   make all

Тестирование
============
Для запуска автоматических тестов выполните команду:

.. code-block:: console
    make test
Отчет о тестировании находится в файле `src/htmlcov/index.html`.

Документация
============

Клиенты
=======
base
--------
.. automodule:: clients.base.base
    :members:

Geo
---
.. automodule:: clients.geo
    :members:

Schemas
-------
.. automodule:: clients.base.base
    :members:

Integrations
============
Database
--------
.. automodule:: integrations.db.session
    :members:
Events
------
.. automodule:: integrations.events.events
    :members:
.. automodule:: integrations.events.schemas
    :members:

Models
======
.. automodule:: models.mixins
    :members:
.. automodule:: models.places
    :members:
Repositories
============
.. automodule:: repositories.base_repository
    :members:
.. automodule:: repositories.places_repository
    :members:


Settings
========
.. automodule:: settings
    :members:

Schemas
=======
.. automodule:: schemas.base
    :members:
.. automodule:: schemas.places
    :members:
.. automodule:: schemas.routes
    :members:

Services
========
.. automodule:: services.places_service
    :members:

Transport
=========
.. automodule:: transport.handlers.places
    :members:
