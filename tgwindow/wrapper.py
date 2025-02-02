from functools import wraps
from typing import TYPE_CHECKING, Union

from aiogram.types import Message, CallbackQuery

from tgwindow.registration import Registration

if TYPE_CHECKING:
    from tgwindow import WindowBase


def auto_window(func):
    """
    Декоратор для автоматической работы с окнами.

    При вызове метода окна:
    1. Создает новый экземпляр окна на основе имени класса метода.
    2. Вызывает переданную функцию (метод окна).
    3. Формирует сообщение и клавиатуру через метод `create_window()`.
    4. Отправляет сообщение с помощью Send.

    Args:
        func: Синхронная функция окна.

    Returns:
        Синхронная обертка функции.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):


        # Извлекаем имя класса (должно быть в нижнем регистре)
        class_name = func.__qualname__.split(".")[0].lower()

        # Регистрация окна
        window = Registration()

        event: Union[Message, CallbackQuery, None] = None
        for arg in args:
            if isinstance(arg, (Message, CallbackQuery)):
                event = arg
                break

        # Создаем экземпляр окна и передаем событие
        self: WindowBase = window.windows[class_name](event)

        # Задаем язык, если он передан в kwargs
        self.lang = kwargs.get("lang", "ru")

        # Вызываем оригинальную функцию
        func(self, *args, **kwargs)

        # Если событие не передано, вызываем create_window и возвращаем данные
        if event is not None:
            self.create_window()
            return

        # Если события не было, создаем окно и подготавливаем данные
        text, reply_markup = self.create_window()

        # Возвращаем данные для отправки (текст, клавиатура, фото)
        data = {
            "text": text,
            "caption": text,
            "reply_markup": reply_markup,
            "photo": self.photo
        }
        return data

    return wrapper
