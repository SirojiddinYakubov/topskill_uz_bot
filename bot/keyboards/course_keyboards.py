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


def get_paginated_course_ikb() -> types.InlineKeyboardMarkup:
    buttons = types.InlineKeyboardMarkup()
    left_button = types.InlineKeyboardButton("←", callback_data="None")
    page_button = types.InlineKeyboardButton("1/4", callback_data="None")
    right_button = types.InlineKeyboardButton("→", callback_data="None")
    buy_button = types.InlineKeyboardButton(_("Sotib olish"), callback_data="None")
    buttons.add(left_button, page_button, right_button)
    buttons.add(buy_button)
    return buttons
