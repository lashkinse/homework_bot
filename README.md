# Телеграм-бот (homework_bot)
![python version](https://img.shields.io/badge/Python-3.9-green)
![python telegram](https://img.shields.io/badge/python--telegram--bot-13.7-green)
![pytest version](https://img.shields.io/badge/pytest-6.2-green)
![requests version](https://img.shields.io/badge/requests-2.26-green)
![sorl-thumbnail version](https://img.shields.io/badge/thumbnail-12.7-green)

Телеграм-бот для отслеживания состояния проверки домашних заданий на платформе Яндекс.Практикум.
Уведомляет пользователей о любых изменениях в статусе проверки, таких как "в процессе проверки", "имеются замечания", "задание выполнено".

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/lashkinse/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Записать в переменные окружения (файл .env) необходимые ключи:
- токен профиля на Яндекс.Практикуме
- токен телеграм-бота
- свой ID в телеграме


Запустить проект:

```
python homework.py
```
