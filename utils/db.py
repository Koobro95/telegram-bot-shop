import json
import os

PRODUCT_FILE = "data/products.json"

def get_products():
    if not os.path.exists(PRODUCT_FILE):
        return []  # Fayl mavjud bo'lmasa, bo'sh ro'yxat qaytaradi
    with open(PRODUCT_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []  # Faylda noto‘g‘ri format bo‘lsa, xatolik chiqmasligi uchun
