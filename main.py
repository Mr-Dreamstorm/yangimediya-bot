import asyncio
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def start(msg: types.Message):
    await msg.answer("🚀 Bot ishlayapti!")

async def main():
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())
