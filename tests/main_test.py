import asyncio

from aiogram import Dispatcher, Bot, F
from aiogram.types import Message, CallbackQuery

from src.middleware import WindowMiddleware
from src.window.base import BaseWindow, Inline, Reply
from src.window.wrapper import auto_window

dp = Dispatcher()


class Example(BaseWindow):
    #Buttons
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



async def main():

    bot = Bot("YOUR_BOT_TOKEN")
    dp.update.middleware(WindowMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



@dp.message(F.text == "/start")
async def hello_mes(msg: Message, example: Example):
    await example.hello(msg, username="belyankiss")

@dp.callback_query(F.data == Example.FIRST_BUTTON.callback)
async def answer_schema(call: CallbackQuery, example: Example):
    await example.schema_buttons(call)

@dp.message()
async def any_message(msg: Message, example: Example):
    await example.inline_button(msg)




if __name__ == '__main__':
    asyncio.run(main())

