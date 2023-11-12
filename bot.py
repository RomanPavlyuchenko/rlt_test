import asyncio
import logging

from aiogram import Bot, Dispatcher

from tgbot.config import config
from tgbot.handlers import register_user


async def main():

    bot = Bot(token=config.tg.token)
    dp = Dispatcher(bot)

    bot.set_current(bot)
    await register_user(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped!")
