import uuid
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Message

from tgwindow import WindowBase, auto_window


@pytest.mark.asyncio
async def test_auto_window():
    """Тест работы декоратора auto_window"""

    from tgwindow import Registration

    class TestWindowUnique(WindowBase):
        @auto_window
        def show(self):
            self.text = "Test Auto Window"

    # Добавляем уникальный идентификатор в имя класса
    class_name = f"TestWindowUnique_{uuid.uuid4().hex}"
    TestWindowUnique.__name__ = class_name

    event = AsyncMock(spec=Message)

    # Регистрируем TestWindowUnique вручную, чтобы избежать конфликта имен
    Registration().add(TestWindowUnique)