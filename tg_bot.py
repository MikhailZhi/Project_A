from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import tg_token

bot = Bot(token=tg_token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def star_def(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Вход в таверну')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def income(message: types.Message):
    if message.text == 'Yes':
        await message.reply(text='Прочесть вывеску "бесплатная кружка"')
    elif message.text == 'No':
        pass
    else:
        pass

if __name__ == '__main__':  # конструкция для запуска бота.
    executor.start_polling(dp, skip_updates=True)
