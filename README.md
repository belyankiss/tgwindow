# TGWindow

**TGWindow** — это библиотека для удобного создания и управления окнами (сообщениями) в **Telegram** с использованием **Aiogram**. Она предоставляет базовый интерфейс для работы с текстом, кнопками и отправкой сообщений. Также можно прикреплять фото к сообщениям.

---

## Возможности библиотеки
- Удобное создание сообщений с текстом и кнопками.
- Поддержка **Inline** и **Reply** клавиатур.
- Гибкая настройка размеров клавиатур.
- Простое взаимодействие с `Message` и `CallbackQuery`.

---

## Установка

Установите библиотеку через `pip` (если она доступна) или вручную.

```bash
pip install tgwindow
```

---

## Пример использования

### 1. **Создание окна и отправка сообщения**

Для начала необходимо запустить самого бота и подключить к нему WindowMiddleware

```python
import asyncio
from aiogram import Dispatcher, Bot
from src.middleware import WindowMiddleware

dp = Dispatcher()

async def main():
    bot = Bot("YOUR_BOT_TOKEN")
    # Здесь подключаем WindowMiddleware
    dp.update.middleware(WindowMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())

```
**Далее создаем окна.**

```python
from src.window.base import BaseWindow, Inline, Reply
from src.window.wrapper import auto_window


class Example(BaseWindow):
    # Buttons
    FIRST_BUTTON = Inline("first", "first_")
    SECOND_BUTTON = Reply("text")
    THIRD_BUTTON = Reply("text")

    @auto_window
    async def hello(self, username: str):
        self.photo = "Path:/to/your/photo.jpg"
        self.text = f"Привет {username}"
        self.buttons(self.SECOND_BUTTON,
                     self.THIRD_BUTTON)

    @auto_window
    async def schema_buttons(self):
        self.text = "Schema"
        self.buttons("one", "two", "three", "four", "five")
        self.schema_keyboard = 3, 1, 1

    @auto_window
    async def inline_button(self):
        self.text = "This message with inline keyboard"
        self.button(*self.FIRST_BUTTON)

```
**Теперь можно создавать handlers**
```python
from aiogram import F
from aiogram.types import Message, CallbackQuery
from tests.main_test import dp, Example


@dp.message(F.text == "/start")
async def hello_mes(msg: Message, example: Example):
    await example.hello(msg, username="belyankiss")

@dp.callback_query(F.data == Example.FIRST_BUTTON.callback)
async def answer_schema(call: CallbackQuery, example: Example):
    await example.schema_buttons(call)

@dp.message()
async def any_message(msg: Message, example: Example):
    await example.inline_button(msg)
```
*ВНИМАНИЕ!* Чтобы получить доступ к вашему классу в handlers, необходимо использовать название вашего класса в малом регистре!!!
---



## Основные классы

### 1. **`BaseWindow`**
`BaseWindow` — это базовый класс для создания окон. Он предоставляет методы для настройки текста и кнопок.

- **`self.text`** — текст сообщения.
- **`self.size_keyboard(int)`** — настройка количества кнопок в ряду.
- **`self.schema_keyboard(Tuple[int, ...])`** - настройка схемы клавиатуры. Принимает кортеж из целых чисел для необходимого количества кнопок в ряду. Сумма чисел кортежа должна быть равна количеству кнопок.
- **`self.photo(str)`** — принимает путь к файлу фото локально или уникальный идентификатор с серверов телеграмм
- **`self.delete_keyboard(bool)`** - булева для удаления reply-клавиатуры. Изначально False.
- **`self.message()`** - возвращает кортеж. Где 1 значение это текст, 2 - клавиатура или None. Удобно использовать при отправке сообщений напрямую через бот. Тогда декоратор @auto_window использовать не нужно

---


## Требования
- **Python 3.8+**
- **Aiogram 3.0+**

---

## Лицензия
Этот проект распространяется под лицензией **MIT**. Используйте свободно!

---

## Обратная связь
Если у вас есть вопросы или предложения, создавайте **Issue** или отправляйте PR.

---
