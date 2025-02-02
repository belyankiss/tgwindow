from typing import Optional, Literal, Iterable, Any
from aiogram.types import KeyboardButton, InlineKeyboardButton

_CALLBACKS = []
_TEXTS = []


def _saver_callback_data(callback_data: str):
    """
    Сохраняет callback_data, проверяя её на уникальность.

    :param callback_data: Данные для callback
    :raises ValueError: Если callback_data уже существует
    """
    if callback_data in _CALLBACKS:
        raise ValueError(f"Такой callback_data={callback_data} уже существует")
    _CALLBACKS.append(callback_data)


def _saver_texts(text: str):
    """
    Сохраняет текст кнопки, проверяя его на уникальность.

    :param text: Текст кнопки
    :raises ValueError: Если текст кнопки уже существует
    """
    if text in _TEXTS:
        raise ValueError(f"Такой текст {text} кнопки уже существует")
    _TEXTS.append(text)


class Reply:
    """
    Класс для создания кнопки типа ReplyKeyboardButton.

    Этот класс создаёт кнопку с текстом, которая будет отображаться на обычной клавиатуре Telegram.
    """

    def __new__(cls, ru: str, en: str = None):
        """
        Конструктор класса. Инициализирует кнопку с текстом на русском и/или английском языке.

        :param ru: Текст кнопки на русском языке (обязательный параметр)
        :param en: Текст кнопки на английском языке (необязательный параметр)
        :raises ValueError: Если текст кнопки на русском не задан
        """
        if not ru:
            raise ValueError("Текст кнопки не должен быть пустым")
        _saver_texts(ru)
        if en:
            _saver_texts(en)
        _instance = super().__new__(cls)
        _instance.ru = ru
        _instance.en = en
        _instance.lang = None
        _instance.button = None
        return _instance

    def __call__(self, lang: Literal["ru", "en"]) -> KeyboardButton:
        """
        Возвращает кнопку с текстом на указанном языке.

        :param lang: Язык кнопки. Возможные значения: 'ru' или 'en'.
        :return: Объект KeyboardButton с текстом на выбранном языке
        """
        self.lang = lang
        if all([self.ru, self.en]):
            self.button = {"ru": KeyboardButton(text=self.ru), "en": KeyboardButton(text=self.en)}.get(lang)
        else:
            self.button = KeyboardButton(text=self.ru)
        return self.button

    def __contains__(self, text: str) -> bool:
        """
        Проверяет, существует ли указанный текст в тексте кнопки.

        :param text: Текст для поиска в кнопке
        :return: True, если текст найден, иначе False
        """
        return text in [self.ru, self.en]

    def __repr__(self):
        """
        Возвращает строковое представление кнопки.

        :return: Строковое представление кнопки
        """
        self.__call__(self.lang or "ru")
        return f"{self.button}"


class Inline:
    """
    Класс для создания кнопки типа InlineKeyboardButton.

    Этот класс создаёт inline-кнопку с callback-данными или ссылкой.
    """

    def __new__(cls, ru: str, callback_data: Optional[str] = None, en: Optional[str] = None, url: Optional[str] = None):
        """
        Конструктор класса. Инициализирует кнопку с callback-данными или URL и текстом на русском и/или английском языке.

        :param ru: Текст кнопки на русском языке (обязательный параметр)
        :param callback_data: Данные для callback (необязательный параметр)
        :param en: Текст кнопки на английском языке (необязательный параметр)
        :param url: URL для кнопки (необязательный параметр)
        :raises ValueError: Если задано одновременно callback_data и url, или если отсутствует хотя бы один из них
        """
        if url and not url.startswith("https:"):
            raise ValueError("URL должен начинаться с https:")
        if all([callback_data, url]):
            raise ValueError("Необходимо использовать либо callback_data, либо url")
        if not ru:
            raise ValueError("Текст кнопки не должен быть пустым")
        if not callback_data and not url:
            raise ValueError("Добавьте один из параметров: callback_data или url")
        if callback_data:
            _saver_callback_data(callback_data)
        _instance = super().__new__(cls)
        _instance.ru = ru
        _instance.en = en
        _instance.callback_data = callback_data
        _instance.url = url
        _instance.lang = None
        _instance.button = None
        return _instance

    def __call__(self, lang: Literal["ru", "en"]) -> InlineKeyboardButton:
        """
        Возвращает inline кнопку с текстом и параметрами для заданного языка.

        :param lang: Язык кнопки. Возможные значения: 'ru' или 'en'.
        :return: Объект InlineKeyboardButton с текстом и параметром для выбранного языка
        """
        self.lang = lang
        if self.ru and self.en:
            if self.url:
                button = {"ru": InlineKeyboardButton(text=self.ru, url=self.url),
                          "en": InlineKeyboardButton(text=self.en, url=self.url)}.get(lang)
            else:
                button = {"ru": InlineKeyboardButton(text=self.ru, callback_data=self.callback_data),
                          "en": InlineKeyboardButton(text=self.en, callback_data=self.callback_data)}.get(lang)
        else:
            if self.url:
                button = InlineKeyboardButton(text=self.ru, url=self.url)
            else:
                button = InlineKeyboardButton(text=self.ru, callback_data=self.callback_data)
        self.button = button
        return button

    def __contains__(self, callback_data: str) -> bool:
        """
        Проверяет, начинается ли callback_data кнопки с указанной строки.

        :param callback_data: Данные для проверки
        :return: True, если callback_data начинается с указанной строки, иначе False
        """
        return self.callback_data.startswith(callback_data)

    def __eq__(self, callback_data: str) -> bool:
        """
        Проверяет, равна ли callback_data кнопки указанной строке.

        :param callback_data: Данные для проверки
        :return: True, если callback_data равна указанной строке, иначе False
        """
        return self.callback_data == callback_data

    def __repr__(self):
        """
        Возвращает строковое представление кнопки.

        :return: Строковое представление кнопки
        """
        self.__call__(self.lang or "ru")
        return f"{self.button}"


class DynamicKeyboard:
    """
    Класс для динамической клавиатуры.

    Этот класс предоставляет возможность создания клавиатуры с динамическим набором кнопок.
    """
    def __init__(self, data: Iterable[Any]):
        """
        Конструктор класса. Инициализирует динамическую клавиатуру.

        :param data: Данные для создания кнопок
        """
        self.data = data
        # Ожидается, что данные будут преобразованы в кнопки в дальнейшем
        # Реализация не предоставлена в коде


class TextMessage:
    """
    Класс для создания текстового сообщения.

    Этот класс позволяет добавлять текстовые сообщения в статические окна.
    """
    def __init__(self, ru: str, en: Optional[str] = None):
        """
        Конструктор класса. Инициализирует текстовое сообщение с текстом на русском и/или английском языке.

        :param ru: Текст сообщения на русском языке (обязательный параметр)
        :param en: Текст сообщения на английском языке (необязательный параметр)
        :raises AttributeError: Если текст на русском не задан
        """
        if not ru:
            raise AttributeError("Текст не может быть пустым")
        self.text = {
            "ru": ru,
            "en": en
        }

    def __repr__(self):
        """
        Возвращает строковое представление текста сообщения.

        :return: Строковое представление текста сообщения
        """
        return f"{self.text}"

