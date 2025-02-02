import pytest
from unittest.mock import AsyncMock

from aiogram.types import Message

from tgwindow.sender import Send


@pytest.mark.asyncio
async def test_send_message():
    """Тест отправки текстового сообщения"""
    event = AsyncMock(spec=Message)
    # Замокаем асинхронный метод answer
    event.answer = AsyncMock()

    # Теперь тест должен пройти без ошибки
    send = Send(event=event, text="Hello, world!")
    await send.send_to()