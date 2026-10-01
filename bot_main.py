import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import settings
from app.bot.middlewares.db import DbSessionMiddleware
from app.bot.handlers.user import user
from app.bot.handlers.registration import router as registration_router
from app.bot.handlers.feed import router as feed_router

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    dp.update.outer_middleware(DbSessionMiddleware())
    dp.include_router(registration_router)
    dp.include_router(user)
    dp.include_router(feed_router)
    print('Bot successfully started')
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')