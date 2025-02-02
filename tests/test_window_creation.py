from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message

from tgwindow import WindowBase


@pytest.mark.asyncio
async def test_window_creation():
    """Тест создания окна"""
    event = AsyncMock(spec=Message)
    window = WindowBase()
    window.text = "Test Window"

    result = window.create_window()
    assert result == ("Test Window", None)