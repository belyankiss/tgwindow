import logging
import aiofiles

from aiogram.types import (Message,
                           CallbackQuery,
                           ReplyKeyboardMarkup,
                           InlineKeyboardMarkup,
                           ReplyKeyboardRemove,
                           BufferedInputFile)
from pydantic_core import ValidationError



class Send:
    def __init__(self, event: Message | CallbackQuery,
                 text: str,
                 reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | None = None,
                 photo: str = None):
        self.event: Message | CallbackQuery = event
        self.text: str = text
        self.reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | None = reply_markup
        self.photo: str | None = photo

    async def _sender(self) -> Message:
        if isinstance(self.event, Message):
            event = await self._is_message()
        else:
            event = await self._is_callback()
        return event

    async def _is_message(self) -> Message:
        if self.photo is not None:
            event = await self.event.answer_photo(photo=self.photo, caption=self.text, reply_markup=self.reply_markup)
        else:
            event = await self.event.answer(text=self.text, reply_markup=self.reply_markup)
        return event

    async def _is_callback(self) -> Message:
        self.event: CallbackQuery
        try:
            if self.event.message.caption is not None:
                event = await self.event.message.edit_caption(caption=self.text, reply_markup=self.reply_markup)
            else:
                event = await self.event.message.edit_text(text=self.text, reply_markup=self.reply_markup)
        except ValidationError:
            event = await self.event.message.answer(text=self.text, reply_markup=self.reply_markup)
        return event

    async def _reformat_photo(self) -> Message:
        try:
            async with aiofiles.open(file=self.photo, mode="rb") as photo:
                photo_byte = BufferedInputFile(file=await photo.read(), filename="photo")
                self.photo = photo_byte
        except FileNotFoundError:
            return await self.event.answer_photo(photo=self.photo, caption=self.text, reply_markup=self.reply_markup)

    def __repr__(self):
        return f"Event: {type(self.event)} Text: {self.text} Reply markup: {self.reply_markup} Photo: {self.photo}"


    async def __call__(self) -> Message:
        if self.photo is not None:
            await self._reformat_photo()
        return await self._sender()