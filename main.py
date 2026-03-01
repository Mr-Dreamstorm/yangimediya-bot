import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# ================== ROLES ==================
SUPER_ADMINS = {5302627260}
ADMINS = set()

def is_super_admin(uid):
    return uid in SUPER_ADMINS

def is_admin(uid):
    return uid in ADMINS or uid in SUPER_ADMINS

# ================== DATA ==================
CHANNELS = ["@Yangimediya"]

MOVIES = {
    "1": {
        "title": "Fast & Furious",
        "file_id": "BAACAgIAAxkBAAIBQ2X..."  # o‘zing almashtirasan
    }
}

# ================== STATES ==================
ADDING_ADMIN = set()
REMOVING_ADMIN = set()
ADDING_SUPER = set()
REMOVING_SUPER = set()
ADDING_CHANNEL = set()
REMOVING_CHANNEL = set()

# ================== SUB CHECK ==================
async def check_sub(user_id):
    try:
        for ch in CHANNELS:
            member = await bot.get_chat_member(ch, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# ================== START ==================
@dp.message(Command("start"))
async def start(message: types.Message):
    uid = message.from_user.id
    name = message.from_user.first_name

    if not await check_sub(uid):
        buttons = []
        for ch in CHANNELS:
            buttons.append([InlineKeyboardButton(
                text=f"📢 {ch}",
                url=f"https://t.me/{ch.replace('@','')}"
            )])

        buttons.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")])

        await message.answer(
            "❗ Kanal(lar)ga obuna bo‘ling:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
        )
        return

    await message.answer(f"🎬 Salom {name}!\nKino kod yubor (masalan: 1)")

# ================== CHECK ==================
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_btn(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.edit_text("✅ Obuna tasdiqlandi! /start bosing")
    else:
        await call.answer("❌ Hali obuna emassiz", show_alert=True)

# ================== MOVIE ==================
@dp.message(lambda m: m.text and m.text.isdigit())
async def movie_handler(message: types.Message):
    code = message.text.strip()

    if code in MOVIES:
        movie = MOVIES[code]

        await message.answer_video(
            video=movie["file_id"],
            caption=f"🎬 {movie['title']}\nKod: {code}"
        )
    else:
        await message.answer("❌ Kino topilmadi")

# ================== ADMIN PANEL ==================
@dp.message(Command("admin"))
async def admin_panel(message: types.Message):
    if not is_admin(message.from_user.id):
        return await message.answer("⛔ Ruxsat yo‘q")

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanallar", callback_data="channels")],
        [InlineKeyboardButton(text="➕ Admin", callback_data="add_admin")],
        [InlineKeyboardButton(text="➖ Admin", callback_data="remove_admin")],
        [InlineKeyboardButton(text="👑 Super Admin", callback_data="add_super")],
        [InlineKeyboardButton(text="🗑 Super Admin", callback_data="remove_super")]
    ])

    await message.answer("⚙️ Admin panel", reply_markup=kb)

# ================== CHANNEL MENU ==================
@dp.callback_query(lambda c: c.data == "channels")
async def channel_menu(call: types.CallbackQuery):
    text = "📢 Kanallar:\n\n" + "\n".join(CHANNELS)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Qo‘shish", callback_data="add_channel")],
        [InlineKeyboardButton(text="➖ O‘chirish", callback_data="remove_channel")]
    ])

    await call.message.edit_text(text, reply_markup=kb)

# ================== BUTTONS ==================
@dp.callback_query(lambda c: c.data == "add_channel")
async def add_channel_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    ADDING_CHANNEL.add(call.from_user.id)
    await call.message.answer("Kanal yubor: @kanal")

@dp.callback_query(lambda c: c.data == "remove_channel")
async def remove_channel_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    REMOVING_CHANNEL.add(call.from_user.id)
    await call.message.answer("O‘chirish uchun kanal")

@dp.callback_query(lambda c: c.data == "add_admin")
async def add_admin_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    ADDING_ADMIN.add(call.from_user.id)
    await call.message.answer("Admin ID yubor")

@dp.callback_query(lambda c: c.data == "remove_admin")
async def remove_admin_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    REMOVING_ADMIN.add(call.from_user.id)
    await call.message.answer("Admin ID o‘chirish")

@dp.callback_query(lambda c: c.data == "add_super")
async def add_super_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    ADDING_SUPER.add(call.from_user.id)
    await call.message.answer("Super admin ID yubor")

@dp.callback_query(lambda c: c.data == "remove_super")
async def remove_super_btn(call):
    if not is_super_admin(call.from_user.id):
        return await call.answer("⛔", show_alert=True)
    REMOVING_SUPER.add(call.from_user.id)
    await call.message.answer("Super admin ID o‘chirish")

# ================== TEXT HANDLER ==================
@dp.message()
async def universal_handler(message: types.Message):
    uid = message.from_user.id
    text = message.text

    try:
        val = int(text)
    except:
        val = None

    # ADMIN ADD
    if uid in ADDING_ADMIN:
        if val:
            ADMINS.add(val)
            await message.answer("✅ Admin qo‘shildi")
        ADDING_ADMIN.remove(uid)
        return

    # ADMIN REMOVE
    if uid in REMOVING_ADMIN:
        if val:
            ADMINS.discard(val)
            await message.answer("🗑 Admin o‘chirildi")
        REMOVING_ADMIN.remove(uid)
        return

    # SUPER ADD
    if uid in ADDING_SUPER:
        if val:
            SUPER_ADMINS.add(val)
            await message.answer("👑 Super admin qo‘shildi")
        ADDING_SUPER.remove(uid)
        return

    # SUPER REMOVE
    if uid in REMOVING_SUPER:
        if val and val != 5302627260:
            SUPER_ADMINS.discard(val)
            await message.answer("🗑 Super admin o‘chirildi")
        REMOVING_SUPER.remove(uid)
        return

    # CHANNEL ADD
    if uid in ADDING_CHANNEL:
        if text.startswith("@"):
            if text not in CHANNELS:
                CHANNELS.append(text)
                await message.answer("✅ Kanal qo‘shildi")
        ADDING_CHANNEL.remove(uid)
        return

    # CHANNEL REMOVE
    if uid in REMOVING_CHANNEL:
        if text in CHANNELS:
            CHANNELS.remove(text)
            await message.answer("🗑 Kanal o‘chirildi")
        REMOVING_CHANNEL.remove(uid)
        return

# ================== RUN ==================
async def main():
    print("Bot ishga tushdi 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
