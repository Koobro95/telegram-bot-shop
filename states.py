from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_address = State()

class AddProduct(StatesGroup):
    name = State()
    price = State()
    size = State()
    availability = State()
    photo = State()
