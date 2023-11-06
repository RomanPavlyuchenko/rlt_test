from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import link


async def user_start(msg: Message):
    chat_link = link(msg.chat.full_name, msg.chat.user_url)
    await msg.answer(f'Hi {chat_link}!', parse_mode='Markdown')


async def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
