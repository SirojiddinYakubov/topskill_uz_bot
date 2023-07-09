from aiogram import types
from bot.core.babel_config import _
from bot.keyboards.course_keyboards import menu_cb


def get_main_menu_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(_("🛄 Kursni tanlang."), callback_data=menu_cb.new(action='courses')),
        ],
        [
            types.InlineKeyboardButton(_("🤔 Savollarga javob toping."), url="https://topskill.uz/faq"),
        ],
        [
            types.InlineKeyboardButton(_("👋🏼 Aloqa qiling va bepul maslahat oling."),
                                       callback_data=menu_cb.new(action='conclusion'))
        ]
    ])


def go_main_menu():
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(_("⬅️ Bosh menu")))
