import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import crud
from bot.handlers.base_handler import BaseHandler
from bot.keyboards.user_keyboards import get_language_kb, get_main_menu_kb, lang_cb
from bot.states.user_states import UserStatesGroup
from bot.crud.user_crud import user_collection
from bot.core.babel_config import _, babel


class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Register main handlers """
        self.dp.register_message_handler(self.start_command, commands=['start'], state="*")
        self.dp.register_callback_query_handler(self.set_language, lang_cb.filter(action="lang"),
                                                state=UserStatesGroup.lang)

    async def start_command(self, message: types.Message, state: FSMContext):
        logging.info(f"Called start command with params: {message}")
        print(18, user_collection)
        user = await user_collection.find_one({"_id": message.chat.id})
        print(20, user)

        await state.set_state(UserStatesGroup.lang)

        if not user:
            return await self.get_language(message)
        else:
            return await self.get_main_menu(message)

    @classmethod
    async def get_language(cls, message: types.Message):
        text = "Assalomu aleykum. Muloqot tilini tanlang!\n\nЗдравствуйте. Выберите язык общения!"
        await message.answer(text=text, reply_markup=get_language_kb())

    @classmethod
    async def get_main_menu(cls, message: types.Message):
        text = _("<b>Men - topskill botiman.</b>\n\nSizni nima qiziqtiradi?")
        await message.answer(text=text, reply_markup=get_main_menu_kb())

    @classmethod
    async def set_language(cls, callback: types.CallbackQuery, callback_data: dict):
        await crud.user_crud.create_user(_id=callback.from_user.id, lang=callback_data['data'])
        await UserStatesGroup.next()
        await callback.message.delete()
        babel.locale = callback_data['data']
        return await callback.message.answer(_("Til muvaffaqiyatli sozlandi. Endi menga ism familiyangizni jo'nating!"))
