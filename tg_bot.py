# Pars_Sb
# @Pasr_Sb_bot:
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import tg_token

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

chat_id = 0


@dp.message_handler(commands='start')
async def star_def(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await bot.send_message(chat_id=message.chat.id, text='Вы входите в бревенчатое здание таверны.')
    await first_choice()


async def first_choice():
    await bot.send_message(chat_id=chat_id, text='Впереди видна какая-то надпись. Вы подойдете? (да/нет)')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def income(message: types.Message):
    if message.text == 'да':
        # Это бесконечный ответ, т.к. данная функция ловит любое сообщение и не прекращается, пока
        # ты не напишешь код, который развивает действие
        await message.reply(text='Прочесть вывеску "бесплатная кружка"? (да/нет)')
    elif message.text == 'нет':
        await message.reply(text='Удачи в следующий раз.')
        await bot.send_message(chat_id=message.chat.id, text='Вы вернулись ко входу в таверну.')
        await first_choice()


if __name__ == '__main__':  # конструкция для запуска бота.
    executor.start_polling(dp, skip_updates=True)
