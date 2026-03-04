import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# ENV dan token olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Render Environment Variables ni tekshir.")

# Bot va dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start komandasi
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("🚀 Yangimediya bot ishga tushdi!")

# Oddiy xabar uchun test
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("📩 Xabar qabul qilindi")

# Polling
async def main():
    print("Bot ishga tushmoqda...")
    await dp.start_polling(bot)

# Eng muhim qism
if name == "main":
    asyncio.run(main())
