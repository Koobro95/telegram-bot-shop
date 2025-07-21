from aiogram import types, Dispatcher
from config import ADMIN_ID

def register_admin_handlers(dp: Dispatcher):

    @dp.message_handler(commands="admin")
    async def admin_panel(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return await message.answer("⛔ Siz admin emassiz.")
        await message.answer("📊 Admin panel: Buyurtmalar shu yerga yuborilmoqda.")
