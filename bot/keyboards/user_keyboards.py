from aiogram import types
from pydantic.networks import AnyHttpUrl
from aiogram.utils.callback_data import CallbackData
from bot.core.config import settings
from bot.schemas.message_schemas import HomeworkStatusEnum
from bot.core.babel_config import _

lang_cb = CallbackData("lang_cb", 'action', 'data')


def get_main_kb() -> types.ReplyKeyboardMarkup:
    """
        Get ikb for menu
    :return:
    """
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Button 1"))


def get_start_kb() -> types.ReplyKeyboardMarkup:
    """
        Get ikb for menu
    :return:
    """
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("/start"))


def signup_ikb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Ro'yhatdan o'tish", url=f"{settings.FRONT_BASE_URL}/auth/signup")]
    ])


def get_contact_kb() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton("Telefon raqamni ulashish 📲", request_contact=True)
    )


# , one_time_keyboard=True


def redirect_to_hw_kb(status: HomeworkStatusEnum, callback_url: AnyHttpUrl):
    if status == HomeworkStatusEnum.WAITING:
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton("Amaliy ishni tekshirish ->", url=callback_url)
            ]
        ])
    elif status == HomeworkStatusEnum.ACCEPTED or status == HomeworkStatusEnum.REJECTED:
        return types.InlineKeyboardMarkup(inline_keyboard=[
            [
                types.InlineKeyboardButton("Kurator izohini o'qish ->", url=callback_url)
            ]
        ])
    else:
        return None


def get_language_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data=lang_cb.new(action='lang', data='uz')),
            types.InlineKeyboardButton("🇷🇺 Русский", callback_data=lang_cb.new(action='lang', data='ru')),
        ]
    ])


def get_main_menu_kb():
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [
            types.InlineKeyboardButton(_("🤔 Savollarga javob toping."), callback_data="faq"),
            types.InlineKeyboardButton(_("💰 Kursni tanlang."), callback_data="select_course")
        ],
        [
            types.InlineKeyboardButton(_("👋🏼 Aloqa qiling va bepul maslahat oling."), callback_data="conclusion")
        ],
        [
            types.InlineKeyboardButton(_("🤔 Savollarga javob toping."), callback_data="faq"),
            types.InlineKeyboardButton(_("💰 Kursni tanlang."), callback_data="select_course")
        ],
    ])
