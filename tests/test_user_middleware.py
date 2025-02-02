from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message

from tgwindow import UserMiddleware


@pytest.mark.asyncio
async def test_user_middleware():
    """Тест работы middleware"""
    middleware = UserMiddleware()
    handler = AsyncMock()
    event = AsyncMock(spec=Message)
    data = {}

    await middleware(handler, event, data)
    assert data["lang"] == "en"
    handler.assert_awaited()