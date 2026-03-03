import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("🚀 Bot ishlayapti!")

@dp.message()
async def echo(message: types.Message):
    await message.answer("📩 Xabar keldi")

async def main():
    await dp.start_polling(bot)

# ✅ ENG MUHIM JOY
if name == "main":
    asyncio.run(main())
