import json

def get_products():
    with open("data/products.json", "r", encoding="utf-8") as f:
        return json.load(f)
