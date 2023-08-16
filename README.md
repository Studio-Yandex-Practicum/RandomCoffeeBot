# RandomCoffeeBot
```
Навигация
```
## О проекте
Random Coffee bot for the Mattermost
## Установка зависимостей
> **Note**
> Официальная документация: ```https://python-poetry.org/docs/```
> Шпаргалка: ```https://habr.com/ru/articles/593529/```

1. Скронируйте репозиторий на локальную машину:
```
git clone git@github.com:Studio-Yandex-Practicum/RandomCoffeeBot.git
```

2. Установите poetry
```
curl -sSL https://install.python-poetry.org | python3 -
```
> **Warning**
> Не используйте pip install poetry

3. Первичная установка зависимостей
```
poetry install
```
4. Активируйте venv
```
poetry shell
```
> **Warning**
> Если вы работаете в pycharm, то:
> Пройдите в add interpreter и установите Poetry Environment

5. Настроить pre-commit
```
pre-commit install
```
> **Примечание**:
  > Перед каждым коммитом будет запущен линтер и форматтер,
  > который автоматически отформатирует код
  > согласно принятому в команде codestyle.

## Настройка
Настройка .env 
## Запуск
Запуск бота
## Использование
Инструкция по alembic