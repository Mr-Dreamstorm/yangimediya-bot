import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ✅ START komandasi
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("🚀 Bot ishlayapti! /start ishladi")

# oddiy message
@dp.message()
async def echo(message: types.Message):
    await message.answer("📩 Xabar keldi")

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
