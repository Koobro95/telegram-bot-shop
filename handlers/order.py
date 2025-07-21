from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from states import OrderState

def register_order_handlers(dp: Dispatcher):

    @dp.callback_query_handler(lambda c: c.data and c.data.startswith("order_"))
    async def handle_order_callback(callback_query: types.CallbackQuery, state: FSMContext):
        product_id = callback_query.data.split("_")[1]
        await state.update_data(product_id=product_id)
        await callback_query.message.answer("👤 Iltimos, ismingizni yozing.")
        await OrderState.waiting_for_name.set()
        await callback_query.answer()
