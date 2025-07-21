from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from states import OrderState

router = Router()

@router.callback_query(F.data.startswith("order_"))
async def handle_order_callback(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("_")[1]
    await state.update_data(product_id=product_id)
    await callback.message.answer("👤 Iltimos, ismingizni yozing.")
    await state.set_state(OrderState.waiting_for_name)
    await callback.answer()
