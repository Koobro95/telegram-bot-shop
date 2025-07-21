from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import OrderState
from utils.db import get_products

def register_user_handlers(dp: Dispatcher):

    @dp.message_handler(commands="start")
    async def send_start(message: types.Message):
        await message.answer("Assalomu alaykum! 👗 Ayollar kiyimlari do‘koniga xush kelibsiz.\nMahsulotlarni ko‘rish uchun /menu yoki /katalog buyrug‘idan foydalaning.")

    @dp.message_handler(commands=["menu", "katalog"])
    async def show_products(message: types.Message):
        products = get_products()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for product in products:
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f"{product['name']} - {product['price']}",
                    callback_data=f"order_{product['id']}"
                )
            )
        await message.answer("📋 Mahsulotlar roʻyxati:", reply_markup=keyboard)

    @dp.message_handler(state=OrderState.waiting_for_name)
    async def process_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("📞 Endi telefon raqamingizni yuboring.")
        await OrderState.next()

    @dp.message_handler(state=OrderState.waiting_for_phone)
    async def process_phone(message: types.Message, state: FSMContext):
        await state.update_data(phone=message.text)
        await message.answer("📍 Endi manzilingizni yuboring.")
        await OrderState.next()

    @dp.message_handler(state=OrderState.waiting_for_address)
    async def process_address(message: types.Message, state: FSMContext):
        from config import ADMIN_ID
        try:
            await state.update_data(address=message.text)
            data = await state.get_data()

            order_msg = (
                f"🛍 <b>Yangi buyurtma!</b>\n\n"
                f"📦 Mahsulot ID: {data['product_id']}\n"
                f"👤 Ism: {data['name']}\n"
                f"📞 Tel: {data['phone']}\n"
                f"📍 Manzil: {data['address']}")

            await message.bot.send_message(chat_id=ADMIN_ID, text=order_msg, parse_mode="HTML")
            await message.answer("✅ Buyurtmangiz qabul qilindi. Tez orada siz bilan bog‘lanamiz!")
        except Exception as e:
            await message.answer(f"❌ Xatolik yuz berdi: {e}")
        finally:
            await state.finish()
