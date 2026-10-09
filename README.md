# QRKot — API благотворительного фонда с отчётами в Excel

Сервис для фонда поддержки котиков. Фонд открывает целевые проекты, пользователи делают пожертвования, а система сама распределяет деньги между проектами и выгружает отчёт по закрытым сборам на Яндекс Диск.

## Возможности

- **Проекты и пожертвования.** Администратор создаёт и редактирует целевые проекты, авторизованные пользователи делают пожертвования и видят свою историю.
- **Автоматическое инвестирование.** Новое пожертвование сразу распределяется по открытым проектам в порядке их создания: если денег больше, чем нужно проекту, остаток уходит в следующий. Новый проект забирает свободные средства из ранее сделанных пожертвований. Проекты и пожертвования закрываются автоматически.
- **Пользователи.** Регистрация и аутентификация по JWT на FastAPI Users, первый суперпользователь создаётся при запуске из переменных окружения.
- **Отчёт.** Эндпоинт `POST /yandex/` формирует Excel-файл со списком закрытых проектов, отсортированных по скорости сбора, загружает его на Яндекс Диск через REST API и возвращает публичную ссылку.

## Технологии

Python 3.10+, FastAPI, SQLAlchemy 2.0 (async), Alembic, Pydantic 2, FastAPI Users, httpx, xlsxwriter, SQLite (aiosqlite), pytest.

## Как запустить

```bash
git clone https://github.com/Vantied/QRkot-spreadsheets.git
cd QRkot-spreadsheets
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Создайте файл `.env` в корне проекта:

```env
APP_TITLE=QRKot
DESCRIPTION=Благотворительный фонд поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=your_secret_key
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=admin_password
YANDEX_DISK_TOKEN=your_yandex_disk_oauth_token
```

Примените миграции и запустите сервер:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Документация API: http://127.0.0.1:8000/docs. Тесты: `pytest`.

## Что я вынес из проекта

- Асинхронная работа с базой данных и внешними API в FastAPI.
- Бизнес-логика вынесена из эндпоинтов: распределение средств работает как отдельный сервис.
- Интеграция со сторонним API: авторизация по токену, загрузка файла и публикация ссылки.

## Автор

Иван Богатов — [GitHub](https://github.com/Vantied) · Telegram [@Ivan_bogatov55](https://t.me/Ivan_bogatov55)
