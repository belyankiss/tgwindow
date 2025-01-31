# TGWindow

**TGWindow** — это библиотека для удобного создания и управления окнами (сообщениями) в **Telegram** с использованием **Aiogram**. Она предоставляет базовый интерфейс для работы с текстом, кнопками и отправкой сообщений. Также можно прикреплять фото к сообщениям.

---

## Возможности библиотеки
- Удобное создание сообщений с текстом и кнопками.
- Поддержка **Inline** и **Reply** клавиатур.
- Гибкая настройка размеров клавиатур.
- Простое взаимодействие с `Message` и `CallbackQuery`.
- Добавлена поддержка на кнопках английского языка

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
from tgwindow import WindowMiddleware

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
from typing import Literal

from aiogram.types import InlineKeyboardButton, KeyboardButton

from tgwindow import BaseWindow, auto_window, Inline, Reply


class Example(BaseWindow):
    # Buttons
    FIRST_BUTTON = InlineKeyboardButton(text="Button 1", callback_data="button_1")
    SECOND_BUTTON = InlineKeyboardButton(text="Button 2", callback_data="button_2")
    BUTTON_WITH_URL = Inline(text="GitHub project", url="https://github.com/belyankiss/tgwindow")
    THIRD_BUTTON = KeyboardButton(text="Button 3")
    FOUR_BUTTON = Reply(text="Button 4")
    BACK_BUTTON = InlineKeyboardButton(text="BACK", callback_data="start")

    @auto_window
    async def hello(self, username: str, lang: Literal["ru", "en"]):
        """
        Можно добавлять фото и передавать в метод любые аргументы для приятной работы!!!
        Args:
            username: Как пример
            lang: Язык пользователя

        Returns:

        """
        # self.photo = "Path:/to/your/photo.jpg"
        self.text = f"Hello {username}"
        self.button(self.FIRST_BUTTON)
        self.button(self.SECOND_BUTTON)
        # Можно добавлять кнопки с поддержкой языков. Поддерживает ru и en
        self.button(Inline(ru="Привет", en="Hello", callback_data="hello_data", lang=lang))

    @auto_window
    async def reply(self):
        self.text = "This is reply keyboard"
        self.button(self.THIRD_BUTTON)
        self.button(self.FOUR_BUTTON)

    @auto_window
    async def inline_button(self):
        self.text = "This message with inline keyboard"
        self.button(self.BUTTON_WITH_URL)

    @auto_window
    async def with_back_button(self):
        self.text = "Hello again!!!"
        self.button(self.BUTTON_WITH_URL)
        self.button(self.BACK_BUTTON)

    async def for_example(self):
        self.text = "Если вы хотите отправить самостоятельно, без автоотправки!"
        self.button(self.FIRST_BUTTON)
        self.button(self.SECOND_BUTTON)
        self.button(self.BUTTON_WITH_URL)
        self.size_keyboard = 2

```
**Теперь можно создавать handlers**
```python
from aiogram import F
from aiogram.types import Message, CallbackQuery
from tests.main_test import dp, Example


@dp.message(F.text == "/start")
@dp.callback_query(F.data == Example.BACK_BUTTON.callback_data)
async def hello_message(event: Message | CallbackQuery, example: Example):
    username = event.from_user.username
    await example.hello(event, username=username, lang="en")

@dp.callback_query(F.data == Example.SECOND_BUTTON.callback_data)
async def answer_with_reply_keyboard(call: CallbackQuery, example: Example):
    await example.inline_button(call)

@dp.callback_query(F.data == Example.FIRST_BUTTON.callback_data)
async def any_message(msg: Message, example: Example):
    await example.reply(msg)

@dp.message(F.text == Example.THIRD_BUTTON.text)
async def answer_reply_button(msg: Message, example: Example):
    await example.with_back_button(msg)

@dp.message()
async def example_send(msg: Message, example: type[Example]):
    example = example()
    await example.for_example()
    text, reply_markup = example.message()
    await msg.answer(text=text, reply_markup=reply_markup)
```
*ВНИМАНИЕ!* Чтобы получить доступ к вашему классу в handlers, необходимо использовать название вашего класса в малом регистре!!!
---



## Основные классы

### 1. **`BaseWindow`**
`BaseWindow` — это базовый класс для создания окон. Он предоставляет методы для настройки текста и кнопок.

- **`self.text`** — текст сообщения.
- **`self.size_keyboard(int)`** — настройка количества кнопок в ряду.
- **`self.photo(str)`** — принимает путь к файлу фото локально или уникальный идентификатор с серверов телеграмм
- **`self.delete_keyboard(bool)`** - булева для удаления reply-клавиатуры. Изначально False.
- **`self.message()`** - возвращает кортеж. Где 1 значение это текст, 2 - клавиатура или None. Удобно использовать при отправке сообщений напрямую через бот. Тогда декоратор @auto_window использовать не нужно

### 2. **`Inline`**
`Inline` - обертка над классом InlineKeyboardButton с возможностью добавления английского языка
- **`self.text`** - текст кнопки. Будет использоваться он, если нет других параметров.
- **`self.ru`** - текст на русском
- **`self.en`** - текст на английском (обязательно нужно указать параметр **`self.lang`**)
- **`self.lang`** - язык пользователя "ru" или "en"
- **`self.callback_data`** - коллбэк - один из обязательных параметров. Либо он, либо **`self.url`**
- **`self.url`** - https ссылка. Нельзя указывать вместе с **`self.callback_data`**

### 3. **`Reply`**
`Reply` - обертка над классом KeyboardButton с возможностью добавления английского языка
- **`self.text`** - текст кнопки. Будет использоваться он, если нет других параметров.
- **`self.ru`** - текст на русском
- **`self.en`** - текст на английском (обязательно нужно указать параметр **`self.lang`**)
- **`self.lang`** - язык пользователя "ru" или "en"



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
