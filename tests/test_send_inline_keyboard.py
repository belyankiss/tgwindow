from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message, InlineKeyboardMarkup

from tgwindow import Inline
from tgwindow.sender import Send


@pytest.mark.asyncio
async def test_send_inline_keyboard():
    """Тест отправки сообщения с inline-клавиатурой"""
    event = AsyncMock(spec=Message)
    # Замокаем асинхронный метод answer
    event.answer = AsyncMock()

    # Создаем объект Send с клавиатурой и текстом
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[Inline("Button", "test_callback")("ru")]])
    send = Send(event=event, text="Choose", keyboard=keyboard)

    # Теперь тест должен пройти без ошибки
    await send.send_to()