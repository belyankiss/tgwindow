from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message

from tgwindow.sender import Send


@pytest.mark.asyncio
async def test_send_photo():
    """Тест отправки фото"""
    event = AsyncMock(spec=Message)
    # Замокаем асинхронный метод answer_photo
    event.answer_photo = AsyncMock()

    # Теперь тест должен пройти без ошибки
    send = Send(event=event, text="Photo", photo=b"image_bytes")
    await send.send_to()