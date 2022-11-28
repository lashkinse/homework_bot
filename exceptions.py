class TelegramSendMessageError(Exception):
    """Ошибка при отправке сообщения"""


class YandexConnectionError(Exception):
    """Ошибка при запросе к эндпоинту API-сервиса"""


class YandexInvalidResponseError(Exception):
    """Не удалось получить ответ от API-сервиса"""


class YandexEmptyResponseError(Exception):
    """Пустой ответ от API-сервиса"""
