from aiogram import Router, F
from aiogram.types import Message
import json
import os

router = Router()

PRODUCT_FILE = "products.json"

def load_products():
    if not os.path.exists(PRODUCT_FILE):
        return []

    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@router.message(F.text.in_(['/menu', '/katalog']))
async def show_products(msg: Message):
    products = load_products()

    if not products:
        return await msg.answer("⛔ Mahsulotlar roʻyxati boʻsh.")

    for product in products:
        caption = (
            f"🆔 ID: {product.get('id')}\n"
            f"📦 Nomi: {product.get('name')}\n"
            f"💵 Narxi: {product.get('price')} so‘m\n"
            f"📏 O‘lcham: {product.get('size')}\n"
            f"✅ Mavjud: {'Ha' if product.get('available') else 'Yo‘q'}"
        )

        # Agar photo mavjud bo‘lsa — rasm bilan chiqarsin
        if "photo" in product:
            try:
                await msg.answer_photo(
                    photo=product["photo"],
                    caption=caption
                )
            except Exception as e:
                await msg.answer(f"⚠️ Rasm chiqarishda xatolik:\n{caption}")
        else:
            # Rasm bo‘lmasa faqat matn
            await msg.answer(caption)
