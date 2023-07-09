import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot import crud
from bot.core.babel_config import _, babel

from bot.crud.user_crud import user_collection
from bot.handlers.base_handler import BaseHandler
from bot.keyboards.course_keyboards import menu_cb
from bot.keyboards.main_keyboards import get_main_menu_kb
from bot.keyboards.user_keyboards import get_language_kb, lang_cb
from bot.states.user_states import UserStatesGroup


class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        """ Register main handlers """
        super().__init__(*args, **kwargs)
        self.dp.register_message_handler(self.start_command, commands=['start'], state="*")
        self.dp.register_callback_query_handler(self.set_language, lang_cb.filter(action="lang"),
                                                state=UserStatesGroup.lang)
        self.dp.register_message_handler(self.go_main_menu, Text(equals="⬅️ Bosh menu"))
        self.dp.register_callback_query_handler(self.conclusion, menu_cb.filter(action="conclusion"))

    async def start_command(self, message: types.Message, state: FSMContext):
        from bot.core.handler import user_handler
        logging.info(f"Called start command with params: {message}")
        print(18, user_collection)
        user = await user_collection.find_one({"_id": message.from_user.id})
        print(20, user)

        if not user:
            user = await crud.user_crud.create_user(_id=message.from_user.id)

        if 'lang' not in user:
            await state.set_state(UserStatesGroup.lang)
            return await self.get_language(message)
        if 'name' not in user:
            await state.set_state(UserStatesGroup.name)
            return await user_handler.get_name(message)
        if 'phone' not in user or 'is_verified' not in user:
            await state.set_state(UserStatesGroup.phone)
            return await user_handler.request_phone(message)

        return await self.go_main_menu(message)

    @classmethod
    async def get_language(cls, message: types.Message):
        text = "Assalomu aleykum. Muloqot tilini tanlang!\n\nЗдравствуйте. Выберите язык общения!"
        await message.answer(text=text, reply_markup=get_language_kb())

    @classmethod
    async def go_main_menu(cls, message: types.Message):
        text = _("<b>Men - topskill botiman.</b>\n\nSizni nima qiziqtiradi?")
        await message.answer(text=text, reply_markup=get_main_menu_kb())

    @classmethod
    async def set_language(cls, callback: types.CallbackQuery, callback_data: dict):
        await crud.user_crud.update_user(_id=callback.from_user.id, lang=callback_data['data'])
        await UserStatesGroup.next()
        await callback.message.delete()
        babel.locale = callback_data['data']
        return await callback.message.answer(_("Til muvaffaqiyatli sozlandi. Endi menga ismingizni jo'nating!"))

    @classmethod
    async def conclusion(cls, callback: types.CallbackQuery, callback_data: dict):
        return await callback.message.answer(
            _("So'rovingiz qabul qilindi! Tez oraqa mutaxasislarimiz siz bilan bog'lanishadi!"))
