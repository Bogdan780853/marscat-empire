import os
import sqlite3
from aiogram import Bot, Dispatcher, types, executor

API_TOKEN = os.getenv("BOT_TOKEN", "")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# SQLite DB
conn = sqlite3.connect("marscat.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    likes INTEGER DEFAULT 0
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS cats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    cat_name TEXT
)
""")
conn.commit()

@dp.message_handler(commands=['start'])
async def start_game(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                       (user_id, username, first_name))
        cursor.execute("INSERT INTO profiles (user_id, likes) VALUES (?, ?)", (user_id, 0))
        cursor.execute("INSERT INTO cats (user_id, cat_name) VALUES (?, ?)", (user_id, 'Базовый Кот'))
        conn.commit()
        await message.answer(f"Привет, {first_name}! Добро пожаловать в Mars Cat Empire!")
    else:
        await message.answer("Ты уже зарегистрирован в Империи Котов!")

@dp.message_handler(commands=['pet'])
async def pet(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("UPDATE profiles SET likes = likes + 5 WHERE user_id = ?", (user_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM profiles WHERE user_id = ?", (user_id,))
    likes = cursor.fetchone()[0]
    await message.answer(f"Ты погладил кота! +5 лайксов. Всего: {likes}")

@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT likes FROM profiles WHERE user_id = ?", (user_id,))
    likes = cursor.fetchone()[0]
    await message.answer(f"Твой профиль:\nЛайксы: {likes}")

@dp.message_handler(commands=['cats'])
async def cats(message: types.Message):
    user_id = message.from_user.id
    cursor.execute("SELECT cat_name FROM cats WHERE user_id = ?", (user_id,))
    cat_list = cursor.fetchall()
    cat_names = "\n".join(f"- {cat[0]}" for cat in cat_list)
    await message.answer(f"Твои коты:\n{cat_names}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)