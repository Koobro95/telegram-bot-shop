from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID
from states import AddProduct
import json
import os

router = Router()

PRODUCT_FILE = "products.json"

def load_products():
    if not os.path.exists(PRODUCT_FILE):
        return []
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_products(products):
    with open(PRODUCT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

@router.message(F.text == "/addproduct")
async def add_product_start(msg: Message, state: FSMContext):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("Sizda bu buyruqni bajarish uchun ruxsat yo‘q.")
    await msg.answer("Tovar nomini kiriting:")
    await state.set_state(AddProduct.name)

@router.message(AddProduct.name)
async def add_product_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Tovar narxini so‘mda kiriting (masalan: 120000):")
    await state.set_state(AddProduct.price)

@router.message(AddProduct.price)
async def add_product_price(msg: Message, state: FSMContext):
    if not msg.text.isdigit():
        return await msg.answer("Iltimos, faqat raqam kiriting:")
    await state.update_data(price=int(msg.text))
    await msg.answer("Tovar o‘lchamini kiriting (masalan: S, M, L):")
    await state.set_state(AddProduct.size)

@router.message(AddProduct.size)
async def add_product_size(msg: Message, state: FSMContext):
    await state.update_data(size=msg.text)
    await msg.answer("Tovar mavjudmi? (ha/yo‘q):")
    await state.set_state(AddProduct.availability)

@router.message(AddProduct.availability)
async def add_product_available(msg: Message, state: FSMContext):
    available = msg.text.lower() in ["ha", "bor", "mavjud", "yes"]
    data = await state.get_data()

    products = load_products()
    new_id = str(len(products) + 1)
    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "size": data["size"],
        "available": available
    }
    products.append(new_product)
    save_products(products)

    await msg.answer(f"✅ Tovar muvaffaqiyatli qo‘shildi!\n\n🆔 ID: {new_id}\n📦 {data['name']}\n💵 Narx: {data['price']} so‘m\n📏 O‘lcham: {data['size']}\n✅ Mavjud: {'Ha' if available else 'Yo‘q'}")
    await state.clear()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Siz admin emassiz.")
    await message.answer("📊 Admin panel: Buyurtmalar shu yerga yuborilmoqda.")

@router.message(AddProduct.availability)
async def add_product_available(msg: Message, state: FSMContext):
    available = msg.text.lower() in ["ha", "bor", "mavjud", "yes"]
    await state.update_data(available=available)
    await msg.answer("📸 Endi tovar rasmi (yoki rasm havolasini) yuboring:")
    await state.set_state(AddProduct.photo)

@router.message(AddProduct.photo)
async def add_product_photo(msg: Message, state: FSMContext):
    if not msg.photo:
        return await msg.answer("❗ Iltimos, tovar rasmini rasm sifatida yuboring.")

    photo_file_id = msg.photo[-1].file_id  # eng sifatli rasm
    await state.update_data(photo=photo_file_id)

    data = await state.get_data()
    products = load_products()
    new_id = str(len(products) + 1)

    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "size": data["size"],
        "available": data["available"],
        "photo": data["photo"]
    }

    products.append(new_product)
    save_products(products)

    await msg.answer_photo(
        photo=data["photo"],
        caption=f"✅ Tovar qo‘shildi!\n\n🆔 ID: {new_id}\n📦 {data['name']}\n💵 {data['price']} so‘m\n📏 O‘lcham: {data['size']}\n✅ Mavjud: {'Ha' if data['available'] else 'Yo‘q'}"
    )

    await state.clear()

