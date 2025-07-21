import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import user, order, admin

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlarni registratsiya qilish
    dp.include_router(user.router)
    dp.include_router(order.router)
    dp.include_router(admin.router)

    # Botni ishga tushirish
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
