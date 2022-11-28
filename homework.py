import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RETRY_PERIOD = 600
ENDPOINT = "https://practicum.yandex.ru/api/user_api/homework_statuses/"
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}

HOMEWORK_VERDICTS = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания.",
}


def init_logger():
    """
    Инициализирует лог
    """
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().addHandler(handler)


def check_tokens():
    """
    Проверяет доступность переменных окружения, которые необходимы для
    работы программы.
    """
    return PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID


def send_message(bot, message):
    """
    Отправляет сообщение в Telegram чат, определяемый переменной
    окружения TELEGRAM_CHAT_ID
    """
    try:
        logging.debug(f"Отправка сообщения: {message}")
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except telegram.TelegramError as error:
        error_message = f"Не удалось отправить сообщение {error}"
        logging.error(error_message)
        raise exceptions.TelegramSendMessageError(error_message)
    else:
        logging.debug(f"Сообщение {message} успешно отправлено")


def get_api_answer(timestamp):
    """
    Делает запрос к эндпоинту API-сервиса
    """
    params = {
        "url": ENDPOINT,
        "headers": HEADERS,
        "params": {"from_date": timestamp},
    }
    try:
        logging.debug(f"Начало запроса: {params}")
        response = requests.get(**params)
        if response.status_code != HTTPStatus.OK:
            raise exceptions.YandexInvalidResponseError(
                f"Не удалось получить ответ от API-сервиса, код ошибки: "
                f"{response.status_code}"
            )
        result = response.json()
        logging.debug(f"Запрос успешно получен: {result}")
        return result
    except Exception as error:
        raise exceptions.YandexConnectionError(
            f"Ошибка при запросе к эндпоинту API-сервиса: {error}"
        )


def check_response(response):
    """
    Извлекает из информации о конкретной домашней работе статус этой работы
    """
    logging.debug("Начало проверки ответа API-сервиса")
    if not isinstance(response, dict):
        raise TypeError("Ошибка в типе ответа API")
    if "homeworks" not in response or "current_date" not in response:
        raise exceptions.YandexEmptyResponseError(
            "Пустой ответ от API-сервиса"
        )
    homeworks = response.get("homeworks")
    if not isinstance(homeworks, list):
        raise TypeError("Homeworks не является списком")
    logging.debug("Проверка ответа API-сервиса выполнена успешно")
    return homeworks


def parse_status(homework):
    """
    Проверяет ответ API на соответствие документации
    """
    if "homework_name" not in homework:
        raise KeyError("В ответе отсутствует ключ homework_name")
    homework_name = homework.get("homework_name")
    if "status" not in homework:
        raise KeyError("В ответе отсутствует ключ status")
    homework_status = homework.get("status")
    if homework_status not in HOMEWORK_VERDICTS:
        raise ValueError(f"Неизвестный статус работы - {homework_status}")
    verdict = HOMEWORK_VERDICTS[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """
    Основная логика работы бота
    """
    if not check_tokens():
        logging.critical("Не заданы одна или несколько переменных окружения")
        sys.exit(0)
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_data = int(time.time())
    prev_message = None
    while True:
        try:
            api_answer = get_api_answer(current_data)
            new_homeworks = check_response(api_answer)
            current_data = api_answer.get("current_data", current_data)
            if new_homeworks:
                message = parse_status(new_homeworks[0])
                if message != prev_message:
                    send_message(bot, message)
                    prev_message = message
            else:
                logging.debug("Статус проверки работы не изменился")
        except exceptions.TelegramSendMessageError as error:
            logging.error(f"Ошибка при отправке сообщения в Telegram: {error}")
        except Exception as error:
            error_message = f"Сбой в работе программы: {error}"
            logging.error(error_message)
            send_message(bot, error_message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == "__main__":
    init_logger()
    main()
