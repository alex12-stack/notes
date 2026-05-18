# 📝 Notes API

**Notes API** — backend-приложение для работы с заметками, пользователями и доступами к заметкам.

Проект реализован на **FastAPI** с использованием **PostgreSQL**, **SQLAlchemy**, **Alembic**, **JWT-аутентификации** и тестов на **pytest**.

---

## 🚀 Стек технологий

- **Python 3**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Alembic**
- **Pydantic**
- **JWT**
- **Pytest**
- **Docker / Docker Compose**
- **Redis / Celery**
- **Git / GitHub**
- **Ruff / Pyright**
- **Logging**

---

## ⚙️ Возможности проекта

- Регистрация и авторизация пользователей
- JWT-аутентификация
- CRUD-операции для заметок
- Управление доступами к заметкам
- Работа с PostgreSQL через SQLAlchemy ORM
- Миграции базы данных через Alembic
- Валидация данных через Pydantic-схемы
- Тестирование ключевых сценариев через pytest
- Автоматическая Swagger/OpenAPI-документация
- Разделение проекта на слои: routers, schemas, models, services, repositories
- Логирование ошибок и ключевых операций
- Подготовка проекта к запуску через Docker Compose

---

## 🗂 Архитектура проекта

```text
src/
├── api/                 # API-роутеры
├── core/                # Конфигурация приложения
├── models/              # SQLAlchemy-модели
├── schemas/             # Pydantic-схемы
├── services/            # Бизнес-логика
├── repositories/        # Работа с базой данных
├── migrations/          # Alembic-миграции
└── main.py              # Точка входа приложения

tests/                   # Тесты
alembic.ini              # Конфигурация Alembic
requirements.txt         # Зависимости проекта
README.md                # Описание проекта