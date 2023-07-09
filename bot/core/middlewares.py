import logging
from typing import Callable

from fastapi import Request

from bot.core.babel_config import babel, ALLOWED_LANGUAGES
from bot.crud.user_crud import user_collection
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class GetAcceptLanguageMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            user_data = await user_collection.find_one({'_id': message.from_user.id})
            if user_data:
                lang = user_data['lang']
            else:
                lang = ALLOWED_LANGUAGES[0]
        except Exception as e:
            logging.error(str(e))
            lang = ALLOWED_LANGUAGES[0]

        if lang not in ALLOWED_LANGUAGES:
            lang = ALLOWED_LANGUAGES[0]

        print(15, lang)
        babel.locale = lang
