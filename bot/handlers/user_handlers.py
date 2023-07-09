import logging

import pyotp
from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import crud
from bot.core.babel_config import _
from bot.core.config import settings

from bot.crud import user_crud
from bot.handlers.base_handler import BaseHandler
from bot.keyboards.user_keyboards import get_contact_kb
from bot.states.user_states import UserStatesGroup
from bot.utils.sms_client import eskiz_auth


class UserHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret = None
        """ Register user handlers """
        self.dp.register_message_handler(self.set_name, lambda m: len(m.text) > 3, state=UserStatesGroup.name)
        self.dp.register_message_handler(self.invalid_name, lambda m: len(m.text) <= 3, state=UserStatesGroup.name)

        self.dp.register_message_handler(self.request_phone, state=UserStatesGroup.phone)
        self.dp.register_message_handler(self.save_phone, state=UserStatesGroup.phone,
                                         content_types=types.ContentType.CONTACT)

        self.dp.register_message_handler(self.check_confirm_code, state=UserStatesGroup.confirm_code)

    @classmethod
    async def get_name(cls, message: types.Message):
        return await message.answer(_("Iltimos menga ismingizni jo'nating!"))

    @classmethod
    async def set_name(cls, message: types.Message):
        await crud.user_crud.update_user(_id=message.from_user.id, name=message.text)
        await UserStatesGroup.next()
        return await message.reply(
            _("{name}, telefon raqamingizni ulashing!").format(
                name=message.text), reply_markup=get_contact_kb())

    @classmethod
    async def invalid_name(cls, message: types.Message):
        return await message.reply(_("Ism kamida 3 ta harfdan iborat bo'lishi kerak!"))

    async def save_phone(self, message: types.Message):
        phone = message.contact.phone_number
        if "+" in phone:
            phone = phone.replace("+", "")
        await crud.user_crud.update_user(_id=message.from_user.id, phone=phone)

        await UserStatesGroup.next()

        await self.send_otp_code(message, phone)

        return await message.reply(_("{phone} raqamiga sms kod jo'natildi. Sms kodni kiriting:").format(phone=phone))

    @classmethod
    async def request_phone(cls, message: types.Message):
        return await message.reply(_("Iltimos telefon raqamingizni ulashing!"),
                                   reply_markup=get_contact_kb())

    async def send_otp_code(self, message: types.Message, phone: str):
        try:
            sms_client = eskiz_auth()
            secret = pyotp.random_base32()
            self.secret = secret
            totp = pyotp.TOTP(secret, interval=settings.OTP_CODE_VALID_SECONDS)
            otp = totp.now()

            await sms_client.send_sms(phone=phone,
                                      message=_("Tasdiqlash kodi: {otp}\nhttps://t.me/topskill_uz_bot").format(otp=otp),
                                      created_by_id=message.from_user.id)
            logging.info(f"Confirmation code: {otp}")
        except Exception as e:
            await self.bot.send_message(message.from_user.id, f"Otp code send error: {e}")

    async def check_confirm_code(self, message: types.Message, state: FSMContext):
        from bot.core.handler import main_handler
        sms_code = message.text.zfill(6)
        print(sms_code)
        totp = pyotp.TOTP(self.secret, interval=settings.OTP_CODE_VALID_SECONDS)
        if totp.verify(sms_code):
            await crud.user_crud.update_user(_id=message.from_user.id, is_verified=True)

            await state.finish()

            return await main_handler.go_main_menu(message)
        else:
            return await message.answer(_("Tasdiqlash kodi noto'g'ri!"))
