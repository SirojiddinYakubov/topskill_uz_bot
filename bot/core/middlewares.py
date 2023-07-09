import logging
from typing import Callable

from fastapi import Request

from bot.core.babel_config import babel, ALLOWED_LANGUAGES
from bot.crud.user_crud import user_collection
from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware


class GetAcceptLanguageMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        await self.set_lang(message.from_user.id)

    async def on_process_callback_query(self, callback: types.CallbackQuery, data: dict):
        await self.set_lang(callback.from_user.id)

    @classmethod
    async def set_lang(cls, user_id: int):
        try:
            user_data = await user_collection.find_one({'_id': user_id})
            if user_data and 'lang' in user_data:
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
