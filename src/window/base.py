from collections import namedtuple

from src.errors import EmptyTextError, InlineKeyboardError, WrongFormatError, WrongKeyboardSchema
from src.keyboard.base_keyboard import  BaseKeyboard

from typing import Union, Tuple, NamedTuple
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove


class BaseWindow:
    def __init__(self):
        """
        text - текст сообщения. Поле не может быть пустым.
        """
        self.text: str | None = None
        self._reply: list[str] = []
        self._inline: dict[str, str] = {}
        self.size_keyboard: int = 1
        self.schema_keyboard: Tuple[int, ...] | None = None
        self.photo: str | None = None
        self.delete_keyboard: bool = False

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        window = RegisterWindow()
        window.add(cls)

    def button(self, text: str, callback: str | None = None) -> None:
        """Добавляет одну кнопку."""
        if callback is not None:
            self._inline[text] = callback
        else:
            self._reply.append(text)

    def buttons(self, *buttons: Union[str, tuple[str, str], NamedTuple]) -> None:
        """Добавляет несколько кнопок."""
        for button in buttons:
            if isinstance(button, str):
                self._reply.append(button)
            elif isinstance(button, Reply):
                self._reply.append(button.text)
            elif isinstance(button, (tuple, Inline)):
                if len(button) != 2:
                    raise InlineKeyboardError("Инлайн кнопка должна иметь только 2 значения")
                self._inline[button[0]] = button[1]
            else:
                raise WrongFormatError("Неизвестный формат кнопок")


    def message(self) -> tuple[str, InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove]:
        """Возвращает сообщение с клавиатурой."""
        if not self.text:
            raise EmptyTextError("Текст сообщения должен быть обязательно!")

        kb = BaseKeyboard()

        # Проверка на смешение inline и reply кнопок
        if self._reply and self._inline:
            raise WrongFormatError("Должны быть переданы только inline или только reply кнопки")

        keyboard = self._reply if self._reply else self._inline
        size_keyboard = self.size_keyboard
        delete_keyboard = self.delete_keyboard
        schema = self.schema_keyboard

        # Проверка соответствия schema и количества кнопок
        if schema and sum(schema) != len(keyboard):
            raise WrongKeyboardSchema("Сумма схемы должна быть равна количеству кнопок")

        # Генерация клавиатуры и возврат сообщения
        result = self.text, kb(keyboard, size=size_keyboard, delete_keyboard=delete_keyboard, schema=schema)
        return result

    def __repr__(self):
        return (f"Text: {self.text}\n"
                f"Keyboard: {self._reply or self._inline}\n"
                f"Photo: {self.photo}")



class RegisterWindow:
    _instance = None
    windows: dict[str, type["BaseWindow"]] = {}
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def add(cls, window: type["BaseWindow"]):
        cls.windows[window.__name__.lower()] = window

    def __repr__(self):
        return f"{self.windows}"


class Reply(NamedTuple):
   text: str

class Inline(NamedTuple):
    text: str
    callback: str











