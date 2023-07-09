from aiogram.utils.callback_data import CallbackData
from aiogram import types
from bot.core.babel_config import _

menu_cb = CallbackData("menu_cb", 'action')


def get_course_ikb(url: str) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(_("🌐 Saytda ko'rish"), url=url),
        ],
        [
            types.InlineKeyboardButton(_("💳 Sotib olish"), url=url + "#course-payment")
        ]
    ])
