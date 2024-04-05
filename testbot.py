import assistants
import assistant1
import asyncio
import logging
import sys
import time

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.methods.copy_message import CopyMessage
from asgiref.sync import sync_to_async

TOKEN = '6784402675:AAEbX4Y7cPtdcoQrO-61VOzm4OAbiLzadRw'
#TOKEN = '6814889723:AAFRmWHB2_2CvJqnr45769r3kSK7IJTDx4M' #Ualihan
dp = Dispatcher()
msg_count = 0
my_chats = {}

def chats_take():
    global my_chats
    f1 = open("chats.txt", "r")
    while True:
        line = f1.readline()
        if not line or line == "":
            break
        i = line.find("@")
        my_chats[line[:i]] = line[i+1:-1]
        #print("$$$ " + line)
    f1.close()
    return my_chats


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.reply("Сәлеметсіз бе, мен Qalan.kz-тің ақылды ботымын.\nМаған сұрақ қойыңыз, мен жауап беруге тырысамын.")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    global msg_count, my_chats
    #my_chats = chats_take()
    msg = str(message.text)
    chat_id = str(message.chat.id)
    print("msg: " + msg + ", chat_id: " + chat_id)
    '''
    if my_chats.get(chat_id) is not None:
    #if chat_id in my_chats.keys():
        ans, thread_id = await sync_to_async(assistants.check_user)(msg, str(my_chats[chat_id]), 1)
    else:
        ans, thread_id = await sync_to_async(assistants.check_user)(msg, chat_id, 0)
        print("thread_id: " + thread_id)
        f2 = open("chats.txt", "a")
        f2.write(chat_id + "@" + str(thread_id) + '\n')
        f2.close()
        my_chats[chat_id] = str(thread_id)
    '''
    ans = await sync_to_async(assistant1.check_user)(msg, chat_id)
    #ans = GPT4.main1(msg)
    print("ans: " + ans)
    await message.reply(ans)
        #await message.send_copy(chat_id=message.chat.id)
    #except TypeError:
        #await message.answer("Ошибка при попытке ответить")
    msg_count += 1
    #time.sleep(5)


async def main() -> None:
    #chats_take()
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    chats_take()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


