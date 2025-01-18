from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder, KeyboardButton


class BaseKeyboard:
    def __init__(self):
        self.buttons: dict | list | None = None
        self.size = 1
        self.schema = None

    def _reply_kb(self) -> ReplyKeyboardMarkup:
        if self.schema is not None:
            keyboard = []
            _keyboard: list[str] = list(self.buttons)  # Преобразование в список строк
            index = 0
            for count in self.schema:
                # Проверка на выход за пределы списка
                row = [KeyboardButton(text=_keyboard[i]) for i in range(index, min(index + count, len(_keyboard)))]
                keyboard.append(row)
                index += count
            return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

        # Если `schema` = None, то используем `ReplyKeyboardBuilder`
        keyboard = ReplyKeyboardBuilder()
        keyboard.add(*[KeyboardButton(text=text) for text in self.buttons])
        return keyboard.adjust(self.size).as_markup(resize_keyboard=True)

    def _inline_kb(self) -> InlineKeyboardMarkup:
        if self.schema is not None:
            keyboard = []
            _keyboard: list[tuple[str, str]] = list(self.buttons.items())
            index = 0  # Индекс для отслеживания текущей кнопки

            for item in self.schema:
                row = []  # Создаём новую строку
                for _ in range(item):
                    # Проверка, чтобы не выйти за пределы списка кнопок
                    if index >= len(_keyboard):
                        break
                    text, callback = _keyboard[index]
                    button = (InlineKeyboardButton(text=text, url=callback)
                              if callback.startswith("https")
                              else InlineKeyboardButton(text=text, callback_data=callback))
                    row.append(button)
                    index += 1

                # Добавляем строку с кнопками в клавиатуру
                if row:
                    keyboard.append(row)

            return InlineKeyboardMarkup(inline_keyboard=keyboard)

        keyboard = InlineKeyboardBuilder()
        for text, callback in self.buttons.items():
            if 'https' in callback:
                keyboard.add(InlineKeyboardButton(text=text,
                                                  url=f'{callback}'))
            else:
                keyboard.add(InlineKeyboardButton(text=text,
                                                  callback_data=callback))
        return keyboard.adjust(self.size).as_markup()

    def __call__(self, buttons: dict | list | None = None, schema: tuple = None, size: int = 1,
                 delete_keyboard: bool = False) -> InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove:
        self.buttons = buttons
        self.size = size
        self.schema = schema
        if delete_keyboard:
            return ReplyKeyboardRemove(remove_keyboard=True)
        if isinstance(buttons, list):
            return self._reply_kb()
        elif isinstance(buttons, dict):
            return self._inline_kb()
