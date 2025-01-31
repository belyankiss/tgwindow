from typing import Literal

from aiogram.types import KeyboardButton


class Reply:
    def __new__(cls,
                text: str = None,
                ru: str = None,
                en: str = None,
                lang: Literal["ru", "en"] = None) -> KeyboardButton:
        if not any([text, ru, en]):
            raise ValueError("Добавьте текст (text, ru или en)")

        if lang is None:
            button_text = text or ru or en
        elif all([text, ru, en]) and lang is not None:
            button_text = ru if lang == "ru" else en
        else:
            button_text = text or (ru if lang == "ru" else en)
        if button_text is None:
            raise ValueError(f"Не найден текст для языка {lang}")
        return KeyboardButton(text=button_text)