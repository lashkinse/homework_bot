class SergException(Exception):
    """Кастомное исключение"""


class TelegramSendMessageError(SergException):
    """Ошибка при отправке сообщения"""


class YandexConnectionError(SergException):
    """Ошибка при запросе к эндпоинту API-сервиса"""


class YandexInvalidResponseError(SergException):
    """Не удалось получить ответ от API-сервиса"""


class YandexEmptyResponseError(SergException):
    """Пустой ответ от API-сервиса"""


class YandexDecodingJSONError(SergException):
    """Ошибка при декодировании запроса от API-сервиса"""
