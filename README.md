# Поехали! 🚀

## Установка и настройка виртуального окружения

```bash
python -m venv .venv
```

## Активация окружения

```bash
# Windows:
source .venv/Scripts/activate
# Linux/Mac:
source .venv/bin/activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Установка миграции базы данных

```bash
python manage.py migrate
```

## Создание суперпользователя (администратора)

```bash
python manage.py createsuperuser
```

## Установка русского языка (ru-ru) в настройках

```bash
# Было (по умолчанию)
LANGUAGE_CODE = 'en-us'

# Стало (на русском)
LANGUAGE_CODE = 'ru-ru'
```

## Django Shell Plus

Django Shell Plus - это расширенная интерактивная консоль Django с дополнительными возможностями.

```bash
# Запуск расширенной консоли с автоматическим импортом всех моделей
python manage.py shell_plus

# Запуск с выводом SQL-запросов для отладки
python manage.py shell_plus --print-sql
```

Преимущества shell_plus:

- Автоматический импорт всех моделей проекта
- Автоматический импорт основных модулей Django
- История команд и автодополнение
- Возможность просмотра генерируемых SQL-запросов
- Удобная среда для тестирования кода и работы
