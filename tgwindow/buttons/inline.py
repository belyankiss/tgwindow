from typing import Literal

from aiogram.types import InlineKeyboardButton


class Inline:
    def __new__(cls,
                text: str = None,
                ru: str = None,
                en: str = None,
                callback_data: str = None,
                url: str = None,
                lang: Literal["ru", "en"] = None) -> InlineKeyboardButton:
        if not any([text, ru, en]):
            raise ValueError("Добавьте текст (text, ru или en)")
        if not any([callback_data, url]):
            raise ValueError("Обязательно должен быть или callback_data, или url")
        if callback_data and url:
            raise ValueError("Нельзя передавать одновременно callback_data и url")

        if lang is None:
            button_text = text or ru or en
        elif all([text, ru, en]) and lang is not None:
            button_text = ru if lang == "ru" else en
        else:
            button_text = text or (ru if lang == "ru" else en)
        if button_text is None:
            raise ValueError(f"Не найден текст для языка {lang}")

        return InlineKeyboardButton(text=button_text, callback_data=callback_data or None, url=url or None)