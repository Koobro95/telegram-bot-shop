from aiogram import executor
from loader import dp
import logging
from handlers import user, order, admin

logging.basicConfig(level=logging.INFO)

user.register_user_handlers(dp)
order.register_order_handlers(dp)
admin.register_admin_handlers(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
