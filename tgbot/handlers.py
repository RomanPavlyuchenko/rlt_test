import json

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import link

from .mongo import get_pipeline
from .db import collection


async def user_start(msg: Message):
    chat_link = link(msg.chat.full_name, msg.chat.user_url)
    await msg.answer(f'Hi {chat_link}!', parse_mode='Markdown')


async def get_data(msg: Message):
    user_request = json.loads(msg.text)
    pipeline = get_pipeline(
        date_from=user_request['dt_from'],
        date_to=user_request['dt_upto'],
        group_type=user_request['group_type']
    )
    result_dict = list(collection.aggregate(pipeline))[0]

    await msg.answer(result_dict)


async def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(get_data)
