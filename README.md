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
1. Запустите open-source платформу Mattermost командой
```
docker-compose -f infra/docker-compose.tests.yml up -d
```
2. После запуска контейнера, перейдите на localhost:
```
http://localhost:8065
```
3. Пройдите регестрацию
4. Пройдите в System Console -> Bot Accounts
```
http://localhost:8065/admin_console/integrations/bot_accounts
```
5. Установите все галочки "true"
6. Перейдите по гиперссылке "Integrations>Bot Accounts"
```
http://localhost:8065/{Название команды}/integrations/bots
```
7. Создайте бота. Add Bot Account
> **Note**
> Достаточно задать:
> Username
> Role
8. Скопируйте Token
> **Warning**
> После нажатия Done, вы больше не сможете посмотреть Access Token
9. Создайте в корневой папке .env файл
```
touch .env
```
10. Заполните по примеру со своими значениями
```
BOT_TOKEN=ваш_access_token
BOT_TEAM=название_команды
```
## Запуск
1. Создайте папку logs
> **Warning**
> Без это проект не будет работать
2. Запустите бота командой
На mac/linux
```
python3 src/run.py
```
На Windows
```
python src/run.py
```
> **Warning**
> Не выключайте контейнер с платформой
## Использование
1. Примените миграции базы данных
```
alembic upgrade head
```
