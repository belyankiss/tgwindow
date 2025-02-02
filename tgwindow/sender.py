import logging
from typing import Union

from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup


class Send:
    """
    Класс для отправки сообщений и медиафайлов в Telegram через Aiogram.

    Этот класс обрабатывает отправку сообщений или медиафайлов (фото) как для обычных сообщений, так и для callback-запросов.
    Предусмотрены методы для редактирования сообщений, отправки фото, а также обработки ошибок.
    """

    def __init__(self, event: Union[Message, CallbackQuery],
                 text: str,
                 keyboard: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, None] = None,
                 photo: Union[str, bytes] = None):
        """
        Инициализация объекта отправки.

        :param event: Событие (сообщение или callback-запрос), на которое нужно отправить ответ.
        :param text: Текст сообщения, которое будет отправлено.
        :param keyboard: Клавиатура (Inline или Reply), которая будет прикреплена к сообщению.
        :param photo: Фото для отправки. Может быть строкой (URL) или байтовым объектом.
        """
        self.event = event
        self.text = text
        self.keyboard = keyboard
        self.photo = photo

    async def _edit_text(self):
        """
        Редактирует текст сообщения.
        """
        await self.event.message.edit_text(text=self.text, reply_markup=self.keyboard)

    async def _edit_caption(self):
        """
        Редактирует подпись к фото.
        """
        await self.event.message.edit_caption(caption=self.text, reply_markup=self.keyboard)

    async def _answer_photo(self):
        """
        Отправляет фото в ответ на сообщение или callback-запрос.
        """
        await self.event.answer_photo(caption=self.text, reply_markup=self.keyboard, photo=self.photo)

    async def _answer_message(self):
        """
        Отправляет текстовое сообщение в ответ на сообщение или callback-запрос.
        """
        await self.event.answer(text=self.text, reply_markup=self.keyboard)

    async def _send_photo(self):
        """
        Отправляет фото (при необходимости с подписью) в ответ на сообщение или callback-запрос.
        """
        await self.event.answer_photo(caption=self.text, reply_markup=self.keyboard, photo=self.photo)

    async def _is_message(self):
        """
        Определяет, нужно ли отправлять сообщение или фото, если событие — это сообщение.
        """
        if self.photo is not None:
            await self._send_photo()
            return
        await self._answer_message()

    async def _is_callback(self):
        """
        Определяет, нужно ли редактировать сообщение или отправлять фото, если событие — это callback-запрос.
        """
        if self.photo is not None:
            await self._answer_photo()
            return
        if self.event.message.caption is not None:
            await self._edit_caption()
        else:
            await self._edit_text()

    async def send_to(self):
        """
        Основной метод для отправки сообщения или медиафайла в зависимости от типа события.

        Этот метод вызывает соответствующие методы для отправки сообщения или фото, в зависимости от того,
        является ли событие обычным сообщением или callback-запросом.
        Также обрабатывает ошибки, связанные с невалидными запросами или ограничениями доступа.
        """
        try:
            if isinstance(self.event, Message):
                await self._is_message()
            if isinstance(self.event, CallbackQuery):
                await self._is_callback()
        except TelegramBadRequest as e:
            logging.error(f"TelegramBadRequest: {e}")
        except TelegramForbiddenError as e:
            logging.error(f"TelegramForbiddenError: {e}")
