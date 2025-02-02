from aiogram.types import CallbackQueryfrom aiogram.types import Messagefrom typing import Union

# tgwindow

`tgwindow` — это библиотека для разработки Telegram-ботов с использованием библиотеки `aiogram`. Она предоставляет удобный способ для создания окон с клавишами, обработки пользовательских запросов, а также улучшает взаимодействие с ботами через встроенные миддлвары и статические окна.

## Установка

Для установки библиотеки используйте pip:

```bash
    pip install tgwindow
```

## Описание

Библиотека `tgwindow` представляет собой набор инструментов для создания окон с кнопками, отправки сообщений и обработки запросов с использованием миддлваров в Telegram-ботах. В проекте реализованы следующие ключевые компоненты:

- **Окна (Window)**: Классы, управляющие отображением сообщений и кнопок.
- **Миддлвары (Middleware)**: Логика для обработки пользовательских данных до того, как запрос будет обработан.
- **Регистрация окон**: Позволяет динамически регистрировать окна для обработки.

## Пример использования

### Пример 1: Создание статического окна с кнопками

```python
from tgwindow import StaticWindow, Inline, Reply

class MyWindow(StaticWindow):
    text = "Welcome to My Bot!"
    inline_button = Inline("Inline Button", callback_data="inline")
    second_button = Inline(ru="Вторая кнопка", en="Second button", callback_data="second")
    next_button = Inline(ru="Еще кнопка", en="Any button", url="https://github.com/belyankiss/tgwindow")
    
class ReplyKB(StaticWindow):
   text = "Any text"
   one = Reply(ru="Раз")
   two = Reply(ru="Два", en="Two")

```

### Пример 2: Создание окна

```python
from typing import Union

from aiogram.types import Message, CallbackQuery

from tgwindow import WindowBase, auto_window
from tgwindow.buttons import Reply

class ExampleWindow(WindowBase):

    @auto_window
    def hello(self, *args, photo, **kwargs):
        # нужно писать *args, **kwargs обязательно
        # для отправки фото можете добавить путь к фотографии, либо использовать объект фото телеграмм
        self.photo = "path/to/photo"
        self.photo = photo
        # можете здесь вставлять текст
        self.text = "Любой текст"
        self.en = "Any text"
        
        self.add_window(MyWindow(self.lang))

    @auto_window
    def second(self, event: Union[Message, CallbackQuery], lang: str):
        self.event = event # можно явно указать, но он добавится автоматически
        self.lang = lang # так же можно явно указать. По дефолту ru
        # можно добавить кнопок, но они должны быть одного типа!!!
        self.add_button(Reply(ru="RU", en="EN"))
        self.add_window(ReplyKB(lang))
```

### Пример 3: Использование миддлвара для добавления пользовательских данных

```python
from aiogram import Dispatcher, F
from aiogram.types import Message, CallbackQuery
from tgwindow.middleware import UserMiddleware

dp = Dispatcher(bot)

# Подключение миддлвара для обработки данных пользователя
dp.middleware.setup(UserMiddleware())


@dp.message(F.text == "/start")
# Здесь, чтобы получить доступ к вашему классу, нужно использовать название класса в малом регистре
# lang - язык пользователя. Настраивается в UserMiddleware
async def start(message: Message, examplewindow: ExampleWindow, lang: str):
   # Используем данные, добавленные миддлваром
   # Есть два вида использования:
   # c передачей события:
   examplewindow.hello(message, lang=lang)  # lang указываем обязательно!
   # или можно по-другому:
   await message.answer(**examplewindow.hello(lang=lang))


@dp.callback_query(F.data == MyWindow.inline_button)
# или можно так
@dp.callback_query(F.data.startswith(MyWindow.inline_button))
async def check_callback(call: CallbackQuery, examplewindow: ExampleWindow, lang: str):
    ...
```

### Библиотека также поддерживает уникализацию reply-кнопок и callback_data. Будет возбуждено исключение.




## Структура проекта

```
tgwindow/
│
├── tgwindow/
│   ├── __init__.py          # Главный модуль библиотеки
│   ├── windows.py           # Окна (классы с кнопками и текстами)
│   ├── buttons.py           # Классы для создания кнопок
│   ├── middleware.py        # Миддлвары для обработки пользовательских данных
│   ├── registration.py      # Реестр для регистрации окон
│   ├── static_window.py     # Класс создания статических окон
│   ├── wrapper.py           # декоратор
│   └── sender.py            # Логика для отправки сообщений
│
├── tests/                   # Пример тестов     
│
├── setup.py                 # Конфигурация для установки библиотеки
├── LICENSE                  # Лицензия
└── README.md                # Документация
```

## Как запускать тесты

Для запуска тестов можно использовать `pytest`:

1. Установите необходимые зависимости:

    ```bash
    pip install -r requirements.txt
    ```

2. Запустите тесты:

    ```bash
    pytest
    ```

## Лицензия

MIT
```
