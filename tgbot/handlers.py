import json
import logging
from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import link
from dateutil.relativedelta import relativedelta


from .mongo import get_pipeline
from .db import collection


async def user_start(msg: Message):
    logging.info(
        f'get start from {msg.from_user.id} - {msg.from_user.full_name}'
    )
    chat_link = link(msg.chat.full_name, msg.chat.user_url)
    await msg.answer(f'Hi {chat_link}!', parse_mode='Markdown')


async def get_data(msg: Message):
    logging.info(
        f'get msg from {msg.from_user.id} - {msg.from_user.full_name}'
    )
    logging.info(msg.text)
    try:
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
        response = json.dumps({
            "dataset": filled_values,
            "labels": dates
        })

        logging.info(
            f'send msg to {msg.from_user.id} - {msg.from_user.full_name}'
        )
        logging.info(response)

        await msg.answer(response)

    except Exception as err:
        logging.exception(err)


async def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"])
    dp.register_message_handler(get_data)
