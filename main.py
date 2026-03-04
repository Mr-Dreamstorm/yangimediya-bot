import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode

# ENV dan token olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN topilmadi! Render Environment Variables ni tekshir.")

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


# ====== /start ======
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    text = """
<b>🚀 Yangimediya bot ishga tushdi!</b>

📥 Video yuklash
🎵 Audio ajratish
🔐 Shifrlash
🖼 Konvertor
👑 VIP tizim (tez orada)

Bot ishlayapti ✅
"""
    await message.answer(text)


# ====== Oddiy xabar testi ======
@dp.message()
async def echo_handler(message: types.Message):
    await message.answer("📩 Xabaringiz qabul qilindi")


# ====== Polling ======
async def main():
    print("🚀 Bot ishga tushmoqda...")
    await dp.start_polling(bot)


# ====== ENG MUHIM QISM ======
if name == "main":
    asyncio.run(main())
