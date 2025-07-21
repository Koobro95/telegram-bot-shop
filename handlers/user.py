from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from states import OrderState
from utils.db import get_products
from config import ADMIN_ID

router = Router()

@router.message(F.text == "/start")
async def send_start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👗 Ayollar kiyimlari do‘koniga xush kelibsiz.\n"
        "Mahsulotlarni ko‘rish uchun /menu yoki /katalog buyrug‘idan foydalaning."
    )

@router.message(F.text.in_({"/menu", "/katalog"}))
async def show_products(message: Message):
    products = get_products()

    if not products:
        await message.answer("📭 Hozircha mahsulotlar mavjud emas.")
        return

    for product in products:
        caption = (
            f"📦 <b>{product.get('name', 'Nomaʼlum')}</b>\n"
            f"💵 Narx: {product.get('price', 'Nomaʼlum')} so‘m\n"
            f"📏 O‘lcham: {product.get('size', 'Ko‘rsatilmagan')}\n"
            f"✅ Mavjud: {'Ha' if product.get('available', False) else 'Yo‘q'}"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="🛒 Buyurtma berish",
                callback_data=f"order_{product['id']}"
            )]
        ])

        if 'photo' in product:
            try:
                await message.answer_photo(
                    photo=product['photo'],
                    caption=caption,
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
            except Exception as e:
                await message.answer(
                    text=f"⚠️ Rasm chiqarishda xatolik:\n{caption}",
                    parse_mode="HTML",
                    reply_markup=keyboard
                )
        else:
            await message.answer(
                text=caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )


@router.message(OrderState.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Endi telefon raqamingizni yuboring.")
    await state.set_state(OrderState.waiting_for_phone)


@router.message(OrderState.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("📍 Endi manzilingizni yuboring.")
    await state.set_state(OrderState.waiting_for_address)


@router.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    try:
        await state.update_data(address=message.text)
        data = await state.get_data()

        order_msg = (
            f"🛍 <b>Yangi buyurtma!</b>\n\n"
            f"📦 Mahsulot ID: {data.get('product_id', 'Nomaʼlum')}\n"
            f"👤 Ism: {data.get('name', 'Nomaʼlum')}\n"
            f"📞 Tel: {data.get('phone', 'Nomaʼlum')}\n"
            f"📍 Manzil: {data.get('address', 'Nomaʼlum')}"
        )

        await message.bot.send_message(chat_id=ADMIN_ID, text=order_msg, parse_mode="HTML")
        await message.answer("✅ Buyurtmangiz qabul qilindi. Tez orada siz bilan bog‘lanamiz!")
    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")
    finally:
        await state.clear()
