import os
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import lyricsgenius
import random

# Создаем объект бота и диспетчер
bot = Bot(token="TOKEN")
dp = Dispatcher(bot)

count = 0  # win - player
count2 = 0  # win - bot
count3 = 0  # nobody win

# Создаем объект для работы с API Genius
genius = lyricsgenius.Genius("API_KEY")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Отображение кнопок
    buttons = ["/mini_game", "/help"]
    keyboard.add(*buttons)
    await message.reply(
        "Привет! Я могу определить песню по тексту, который ты написал. Просто отправь мне текст и я постараюсь найти песню. А так же запустить мини-игру по комманде /mini_game. Если у вас есть вопросы, перейдите в раздел /help",
        reply_markup=keyboard)


@dp.message_handler(commands=["help"])
async def send_help(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Отображение кнопок
    buttons = ["/statistica", "/help"]
    keyboard.add(*buttons)
    await message.reply(
        "Просто напишите мне песню и я помогу ее найти, но только чем больше слов из песен вы напишите, тем лучше будет осуществлятся поиск. Так же я могу запустить мини-игру /mini_game.")


@dp.message_handler(commands=["mini_game"])
async def game(message: types.Message):
    global count3, count2, count
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Отображение кнопок
    buttons = ["/statistica", "/next", "/help"]
    keyboard.add(*buttons)
    await message.answer(
        "Здравствуйте! Это простая мини-игра, где бросаются кости и побеждает, тот у кого больше очков, по команде /statistica, вы можете узнать свои результаты.",
        reply_markup=keyboard)
    k1 = random.randint(1, 6)
    k2 = random.randint(1, 6)
    k3 = random.randint(1, 6)
    k4 = random.randint(1, 6)
    if k1 + k2 > k3 + k4:
        count += 1
        await message.answer("Вы победили")
    if k1 + k2 < k3 + k4:
        count2 += 1
        await message.answer("Бот победил")
    if k1 + k2 == k3 + k4:
        count3 += 1
        await message.answer("Ничья")
    await message.reply(f"Побед - {count}, проигрешей - {count2}, ничьей - {count3}. Повтом? Напишите /next")


@dp.message_handler(commands=["next"])
async def game2(message: types.Message):
    global count3, count2, count
    k1 = random.randint(1, 6)
    k2 = random.randint(1, 6)
    k3 = random.randint(1, 6)
    k4 = random.randint(1, 6)
    if k1 + k2 > k3 + k4:
        count += 1
        await message.reply("Вы победили")
    elif k1 + k2 < k3 + k4:
        count2 += 1
        await message.reply("Бот победил")
    else:
        count3 += 1
        await message.reply("Ничья")
    await message.reply(f"Побед - {count}, проигрешей - {count2}, ничьей - {count3}. Повтом? Напишите /next")


@dp.message_handler(commands=["statistica"])
async def stata(message: types.Message):
    await message.reply(f"побед - {count}, проигрешей - {count2}, ничьей - {count3}")


@dp.message_handler()
async def send_lyrics(message: types.Message):
    try:
        text = message.text
        # Ищем песню по тексту
        music = genius.search_song(text)
        flag = False

        # Если песня найдена, отправляем текст песни пользователю
        if music:
            flag = True
            await message.reply(music.lyrics)
        if not flag:
            await message.reply("К сожалению, я не смог найти песню по этому тексту.")
    except:
        await message.reply("К сожалению, я не смог найти песню по этому тексту.")


# Запускаем бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)