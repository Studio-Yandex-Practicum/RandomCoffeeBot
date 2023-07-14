# RandomCoffeeBot

<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#описание">О проекте</a>
      <ul>
        <li><a href="#технологии">Стек технологий</a></li>
      </ul>
    </li>
    <li>
      <a href="#полезная-информация">Полезная информация</a>
      <ul>
        <li><a href="#работа-с-poetry">Работа с Poetry</a></li>
      </ul>
    </li>
  </ol>
</details></br>

## О проекте
Random Coffee bot for the Mattermost

## Стек технологий
[![Python][Python-badge]][Python-url]
[![Poetry][Poetry-badge]][Poetry-url]

## FAQ

Инофрмация для разработчика

<details>
  <summary><h3>Работа с Poetry</h3></summary>

***В этом разделе описана работа с poetry.***

[Подробнее о командах poetry](https://python-poetry.org/docs/cli/)

#### Настройка окружения проекта
Установку необходимо выполнять через curl, как в документации.

    ```shell
    poetry env use python3.9; poetry install
    ```

#### Активировать виртуальное окружение

    ```shell
    poetry shell
    ```

#### Добавить зависимость

    ```shell
    poetry add <package_name>
    ```

> **Note**
> Использование флага `-G dev` позволяет установить зависимость,
> необходимую только для разработки.
> Это полезно для разделения develop и prod зависимостей.

#### Запустить скрипт без активации виртуального окружения

```shell
poetry run <script_name>.py
```
</details>

<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/doc/
[Python-badge]: https://img.shields.io/badge/Python-4682B4?style=for-the-badge&logo=python&logoColor=FFFFFF

[Poetry-url]: https://python-poetry.org/
[Poetry-badge]: https://img.shields.io/badge/poetry-4682B4?style=for-the-badge&logo=poetry&logoColor=FFFFFF
