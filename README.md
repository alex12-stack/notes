# Notes App

Веб-приложение для создания и организации заметок. Пользователь может зарегистрироваться, войти в аккаунт, создавать заметки, распределять их по папкам, редактировать и удалять данные.

Репозиторий проекта: https://github.com/alex12-stack/notes

## Возможности

* регистрация и авторизация пользователей;
* хранение авторизации в cookie;
* создание, редактирование и удаление заметок;
* создание, переименование и удаление папок;
* перенос заметок в категорию «Без папки» при удалении папки;
* разграничение доступа между пользователями;
* поиск заметок;
* HTML-интерфейс на Jinja2;
* документация API через Swagger;
* запуск приложения через Docker Compose.

## Технологический стек

* Python;
* FastAPI;
* Jinja2;
* PostgreSQL;
* SQLAlchemy;
* Alembic;
* Redis;
* Docker;
* Docker Compose;
* Pytest.

## Запуск через Docker Compose

Для запуска нужен установленный и запущенный Docker Desktop.

Склонируйте репозиторий:

```bash
git clone https://github.com/alex12-stack/notes.git
cd notes
```

Запустите проект:

```bash
docker compose up --build
```

При первом запуске Docker автоматически:

1. скачает образы PostgreSQL и Redis;
2. соберёт контейнер FastAPI-приложения;
3. создаст базу данных;
4. применит миграции Alembic;
5. запустит сервер.

После запуска приложение будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Документация API Swagger:

```text
http://127.0.0.1:8000/docs
```

## Остановка приложения

Остановите выполнение сочетанием клавиш:

```text
Control + C
```

Затем выполните:

```bash
docker compose down
```

Данные PostgreSQL сохранятся между перезапусками в Docker volume.

Чтобы удалить контейнеры вместе с данными базы:

```bash
docker compose down -v
```

## Переменные окружения

Для стандартного локального запуска файл `.env` не обязателен: Docker Compose использует значения по умолчанию.

При необходимости настройки можно переопределить. Создайте `.env` на основе примера:

```bash
cp .env.example .env
```

Файл `.env` не должен попадать в публичный репозиторий.

## Запуск без Docker

Для ручного запуска необходимо самостоятельно установить и запустить PostgreSQL и Redis.

Создайте виртуальное окружение:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте `.env`:

```bash
cp .env.example .env
```

При необходимости измените значения подключения к PostgreSQL и Redis.

Примените миграции:

```bash
alembic upgrade head
```

Запустите сервер:

```bash
python -m uvicorn src.main:app --reload
```

## Основные страницы

```text
http://127.0.0.1:8000/app/login
http://127.0.0.1:8000/app/register
http://127.0.0.1:8000/app/notes
http://127.0.0.1:8000/app/folders
```

## Структура проекта

```text
notes/
├── src/
│   ├── api/                 # API-ручки
│   ├── connectors/          # подключение к Redis
│   ├── migrations/          # миграции Alembic
│   ├── models/              # ORM-модели
│   ├── repositories/        # работа с базой данных
│   ├── schemas/             # Pydantic-схемы
│   ├── static/              # CSS и JavaScript
│   ├── templates/           # Jinja2-шаблоны
│   ├── main.py              # точка входа FastAPI
│   └── pages.py             # HTML-страницы
├── tests/                   # тесты
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── README.md
```
