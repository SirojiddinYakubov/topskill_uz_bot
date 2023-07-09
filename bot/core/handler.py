from aiogram import Dispatcher, Bot, types

from bot.core.config import settings
from bot.core.middlewares import GetAcceptLanguageMiddleware
from bot.handlers.course_handlers import CourseHandler
from bot.handlers.user_handlers import UserHandler
from bot.handlers.main_handlers import MainHandler
from aiogram.contrib.fsm_storage.mongo import MongoStorage

storage = MongoStorage(uri=settings.MONGO_URI.replace('/topskill_db', '/aiogram_fsm'))

bot = Bot(token=settings.TOKEN_API, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=storage)

main_handler = MainHandler(dp=dp, bot=bot)
course_handler = CourseHandler(dp=dp, bot=bot)
user_handler = UserHandler(dp=dp, bot=bot)

dp.middleware.setup(GetAcceptLanguageMiddleware())
