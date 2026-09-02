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
