import asyncio
from typing import Optional, Union, Tuple, Literal, TYPE_CHECKING

from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           KeyboardButton,
                           BufferedInputFile, Message, CallbackQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from tgwindow.sender import Send
from tgwindow.registration import Registration


if TYPE_CHECKING:
    from tgwindow.static_window import StaticWindow


class WindowBase:
    """
    Базовый класс для создания окна с клавиатурой и текстом.

    Этот класс управляет отображением текста и кнопок на окне, а также предоставляет
    функциональность для работы с клавиатурами (inline и reply).
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализирует объект окна с начальным состоянием.

        Здесь задаются основные параметры: текст окна, языковая локализация,
        изображение и настройки клавиатуры.
        """
        self.event: Union[Message, CallbackQuery, None] = None
        for arg in args:
            if isinstance(arg, (Message, CallbackQuery)):
                self.event = arg
                break
        self.name = self.__class__.__name__.lower()
        for key, value in kwargs.items():
            if key == "name":
                self.name = value
        self.text: Optional[str] = None
        self.en: Optional[str] = None
        self.lang: Literal["ru", "en"] = "ru"
        self.photo: Optional[str] = None
        self.size_keyboard: Optional[int] = None
        self._inline_buttons: list[list[InlineKeyboardButton]] = []
        self._reply_buttons: list[list[KeyboardButton]] = []

    def __init_subclass__(cls, **kwargs):
        """
        Регистрация дочернего класса в реестре окон.

        При наследовании от этого класса, дочерний класс автоматически регистрируется
        в реестре окон для отслеживания доступных окон.
        """

        registry = Registration()
        registry.add(cls)

    def add_button(self, button: Union[InlineKeyboardButton, KeyboardButton]) -> None:
        """
        Добавляет кнопку в окно.

        Если кнопка inline, то она добавляется в inline-клавиатуру,
        если reply, то в reply-клавиатуру.

        :param button: Кнопка, которая будет добавлена в окно.
        """
        if isinstance(button, InlineKeyboardButton):
            self._inline_buttons.append([button])
        if isinstance(button, KeyboardButton):
            self._reply_buttons.append([button])

    def add_window(self, window: "StaticWindow"):
        """
        Добавляет статическую клавиатуру и текст в окно.

        Клавиатура и текст из переданного объекта StaticWindow добавляются в окно.

        :param window: Класс StaticWindow, который предоставляет набор кнопок для добавления.
        """
        keyboard = window.keyboard
        self.text = window.text

        for button in keyboard:
            if isinstance(button, InlineKeyboardButton):
                self._inline_buttons.append([button])
            if isinstance(button, KeyboardButton):
                self._reply_buttons.append([button])

    def _resize_inline_keyboard(self) -> InlineKeyboardMarkup:
        """
        Применяет настройки размера и возвращает готовую inline клавиатуру.

        :return: Готовая inline клавиатура.
        """
        kb = InlineKeyboardBuilder()
        for button in self._inline_buttons:
            kb.add(button[0])
        return kb.adjust(self.size_keyboard).as_markup()

    def _resize_reply_keyboard(self) -> ReplyKeyboardMarkup:
        """
        Применяет настройки размера и возвращает готовую reply клавиатуру.

        :return: Готовая reply клавиатура.
        """
        kb = ReplyKeyboardBuilder()
        for button in self._reply_buttons:
            kb.add(button[0])
        return kb.adjust(self.size_keyboard).as_markup(resize_keyboard=True)

    def _create_keyboard(self) -> Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None]:
        """
        Создает клавиатуру (inline или reply), если кнопки присутствуют.

        :return: Готовая клавиатура или None, если кнопки не были добавлены.
        """
        if self._inline_buttons:
            return self._resize_inline_keyboard() if self.size_keyboard else InlineKeyboardMarkup(
                inline_keyboard=self._inline_buttons)
        if self._reply_buttons:
            return self._resize_reply_keyboard() if self.size_keyboard else ReplyKeyboardMarkup(
                keyboard=self._reply_buttons, resize_keyboard=True)
        return None

    def _refactor_photo(self):
        """
        Преобразует путь к изображению в формат, подходящий для отправки в Telegram.

        Прочитывает файл изображения и преобразует его в BufferedInputFile для отправки.
        Если файл не найден, пропускает эту операцию.
        """
        if self.photo is not None:
            try:
                with open(file=self.photo, mode="rb") as photo:
                    photo_byte = BufferedInputFile(file=photo.read(), filename="photo")
                    self.photo = photo_byte
            except FileNotFoundError:
                pass

    def create_window(self) -> Tuple[str, Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None]] or None:
        """
        Создает окно с текстом и клавиатурой.

        Проверяет, что текст не пустой, а также если задано изображение, подготавливает его для отправки.

        :return: Текст окна и соответствующая клавиатура (inline или reply).
        :raises AttributeError: Если текст не задан.
        """
        if self.text is None:
            raise AttributeError("Сообщение не может быть пустым! Добавьте текст!")
        self._refactor_photo()
        if self.en is not None and self.lang == "en":
            self.text = self.en
        if self.event is not None:
            send = Send(event=self.event, text=self.text, keyboard=self._create_keyboard(), photo=self.photo)
            asyncio.create_task(send.send_to())
            return None
        return self.text, self._create_keyboard()

    def __repr__(self):
        """
        Строковое представление объекта окна с текстом и клавиатурой.

        :return: Строка с текстом окна и клавиатурой.
        """
        return f"{self.text}\n{self._create_keyboard()}"
