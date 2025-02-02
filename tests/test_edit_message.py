from unittest.mock import AsyncMock

import pytest
from aiogram.types import CallbackQuery

from tgwindow.sender import Send


@pytest.mark.asyncio
async def test_edit_message():
    """Тест редактирования сообщения"""
    event = AsyncMock(spec=CallbackQuery)
    event.message = AsyncMock()
    event.message.caption = None  # Убеждаемся, что caption отсутствует

    send = Send(event=event, text="Updated text")
    await send.send_to()

    event.message.edit_text.assert_called_once_with(text="Updated text", reply_markup=None)