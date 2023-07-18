# Pars_Sb
# @Pasr_Sb_bot:
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import tg_token, drive_file_path
import pandas as pd
import psycopg2
from config import host, user, password, db_name

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

chat_id = 0

# create blank variables just for no errors in auto detection errors
connection = ""
cursor = ""

try:
    # connect to an existing database
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True

    # the cursor for performing database operation
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(f"Server version: {cursor.fetchone()}")

except Exception as ex:
    print("[INFO] Error while working with PostgreSQL", ex)
finally:
    if connection:
        # cursor.close()
        connection.close()
        print("[INFO] PostgreSQL connection closed")


# opening xlsx file
pd.set_option('display.max_rows', None)  # устанавливаю максимальное количество выводимых на экран строк
pd.set_option('display.max_columns', None)  # устанавливаю максимальное количество выводимых на экран столбцов
df = pd.read_excel(drive_file_path, sheet_name='Andrew_scheme')  # при помощи pandas читаем эксель в дата фрейм "df"
last_column = df.shape[0]  # нахожу последнюю строку
last_row = df.shape[1]  # нахожу последнюю колонку

start_point = 'b3'
start_text_loc = 'g3'
start_text = df.iloc[int(start_text_loc[1:len(start_text_loc)]) - 2, ord(start_text_loc[0]) - 97]
# print(start_text)

# room parameters
room_text = ''
room_yes = ''
room_no = ''
room_yes_text = ''
room_no_text = ''


@dp.message_handler(commands='start')
async def star_def(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await bot.send_message(chat_id=message.chat.id, text=start_text)
    await unpack_room_parameters(start_point)


async def unpack_room_parameters(room_number):
    print(f'room_number = {room_number}')
    global room_text, room_yes, room_no, room_yes_text, room_no_text
    room_string = df.iloc[int(room_number[1]) - 2, ord(room_number[0]) - 97]
    print(room_string, '\n')
    room_text_search = room_string.find('text - ') + len('text - ')
    room_text_index = room_string[room_text_search:room_string.find('yes - ') - 1]
    # print(f'room_text_index = {room_text_index}')
    room_yes_search = room_string.find('yes - ') + len('yes - ')
    room_yes = room_string[room_yes_search:room_string.find('- ', room_yes_search + 1) - 1]
    # print(f'room_yes = {room_yes}')
    room_no_search = room_string.find('no - ') + len('no - ')
    room_no = room_string[room_no_search:room_string.find('- ', room_no_search + 1) - 1]
    # print(f'room_no = {room_no}')
    room_yes_text = room_string[room_string.find('- ', room_yes_search + 1) + 2:room_string.find('no - ') - 1]
    print(f'yes text: {room_yes_text}')
    room_no_text = room_string[room_string.find('- ', room_no_search + 1) + 2:len(room_string)]
    print(f'no text: {room_no_text}')
    room_text = df.iloc[int(room_text_index[1:len(room_text_index)]) - 2, ord(room_text_index[0]) - 97]
    # print('i = ', int(room_text_index[1:len(room_text_index)])-2)
    # print(f'column - {ord(room_text_index[0]) - 97}; row - {int(room_text_index[1:len(room_text_index)]) - 2}')
    await bot.send_message(chat_id, text=room_text)
    await bot.send_message(chat_id, text=room_yes_text)
    await bot.send_message(chat_id, text=room_no_text)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def income(message: types.Message):

    if message.text == 'да' or message.text == room_yes_text:
        await unpack_room_parameters(room_yes)
        # Это переброс при ответе "да"

    elif message.text == 'нет' or message.text == room_no_text:
        await unpack_room_parameters(room_no)
        # это переброс при ответе "нет"

if __name__ == '__main__':  # конструкция для запуска бота.
    executor.start_polling(dp, skip_updates=True)
