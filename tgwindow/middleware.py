from typing import Callable, Dict, Any, Awaitable, Type, TYPE_CHECKING
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from tgwindow.registration import Registration


if TYPE_CHECKING:
    from tgwindow import WindowBase


class UserMiddleware(BaseMiddleware):
    """
    Миддлвар для обработки пользовательских данных перед обработкой запроса.

    Этот миддлвар добавляет информацию о языке пользователя и регистрацию окон в контекст данных.
    """

    def __init__(self):
        """
        Инициализация миддлвара.

        В данном конструкторе вызывается инициализация родительского класса.
        """
        super().__init__()
        self.window = Registration()

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any],
                       ) -> Any:
        """
        Основной метод миддлвара. Добавляет информацию о языке и регистрации окон в данные.

        Этот метод выполняет предварительную обработку данных, добавляя в контекст информацию о языке пользователя и
        добавляя зарегистрированные окна в данные.

        :param handler: Обработчик события, которому передаются данные.
        :param event: Событие (сообщение или callback), которое нужно обработать.
        :param data: Данные, которые будут переданы в обработчик.
        :return: Результат выполнения обработчика.
        """


        # Устанавливаем язык пользователя. В реальной ситуации здесь должен быть логика для определения языка.
        data["lang"] = "en"  # Пример: язык установлен на английский (можно заменить на реальную логику)

        # Добавляем окна из реестра в данные. Эти окна будут использоваться в дальнейшем для взаимодействия.
        for key, value in self.window.windows.items():
            key: str
            value: Type["WindowBase"]
            data[key] = value

        # Передаем обработчику результат, полученный после добавления информации о языке и окон.
        return await handler(event, data)
