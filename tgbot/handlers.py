import json
from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import link
from dateutil.relativedelta import relativedelta


from .mongo import get_pipeline
from .db import collection


async def user_start(msg: Message):
    chat_link = link(msg.chat.full_name, msg.chat.user_url)
    await msg.answer(f'Hi {chat_link}!', parse_mode='Markdown')


async def get_data(msg: Message):
    user_request = json.loads(msg.text)
    date_from = user_request['dt_from']
    date_to = user_request['dt_upto']
    group_type = user_request['group_type']

    pipeline = get_pipeline(
        date_from=date_from,
        date_to=date_to,
        group_type=group_type
    )
    result_dict = list(collection.aggregate(pipeline))[0]

    start = datetime.strptime(date_from, '%Y-%m-%dT%H:%M:%S')
    end = datetime.strptime(date_to, '%Y-%m-%dT%H:%M:%S')
    interval = relativedelta(**{group_type+'s': 1})
    dates = list()

    while start <= end:
        dates.append(start.strftime('%Y-%m-%dT%H:%M:%S'))
        start += interval

    filled_values = [
        result_dict[date] if date in result_dict else 0 for date in dates
    ]

    await msg.answer(
        json.dumps({
            "dataset": filled_values,
            "labels": dates
        })
    )


async def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(get_data)
