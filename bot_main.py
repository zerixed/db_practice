import asyncio
from aiogram import Bot, Dispatcher
from config import settings
from app.bot.middlewares.db import DbSessionMiddleware
from app.bot.handlers.user import user
from app.bot.handlers.registration import router as registration_router
async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.include_router(registration_router)
    dp.include_router(user)
    print('Bot successfully started')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')