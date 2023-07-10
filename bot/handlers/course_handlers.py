from bot.core.config import settings

from bot.crud.user_crud import user_collection
from bot.handlers.base_handler import BaseHandler
from aiogram import types
import httpx
from bot.keyboards.course_keyboards import menu_cb, get_course_ikb, get_paginated_course_ikb
from bot.keyboards.main_keyboards import go_main_menu
from bot.core.babel_config import _


class CourseHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Register course handlers """
        self.dp.register_callback_query_handler(self.view_courses, menu_cb.filter(action="courses"))

    async def view_courses(self, callback: types.CallbackQuery, callback_data: dict):
        from bot.core.handler import main_handler
        user = await user_collection.find_one({"_id": callback.from_user.id})
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{settings.FRONT_BASE_URL}/api/v1/site/course/list/?page_size=50")
            if r.status_code == 200:
                for course in r.json()['results']:
                    url = f"{settings.FRONT_BASE_URL}/{user['lang']}/courses/{course['slug']}"
                    if "discount" in course:
                        course_price = course['price'] * (1 - course['discount']['percent'] / 100)
                    else:
                        course_price = course['price']
                    caption = _(
                        """
                        <b>Kurs nomi:</b> <a href='{href_url}'>{course_title}</a>\n<b>Kurs narxi:</b> {course_price:,} so'm\n\n8-qismga bo'lib to'lash orqali <s>{course_price:,}</s> ga emas atigi {part_price:,} so'mga sotib oling. 🔥
                        """
                    ).format(
                        href_url=url,
                        course_title=course['translations'][0]['title'],
                        course_price=int(course_price),
                        part_price=int(course_price * 1.2 // 8)
                    )

                    await self.bot.send_photo(callback.from_user.id,
                                              photo=f"{settings.AWS_BUCKET_URL}{course['banner_image']['path']}",
                                              caption=caption,
                                              reply_markup=get_course_ikb(url=url),
                                              parse_mode="HTML")
                await callback.message.answer(
                    _("{total_results} ta kurs chiqarildi").format(total_results=r.json()['total_results']),
                    reply_markup=types.ReplyKeyboardRemove())
                await main_handler.go_main_menu(callback.message)

    # async def view_course_with_pagination(self, callback: types.CallbackQuery, callback_data: dict):
    # from bot.core.handler import main_handler
    # user = await user_collection.find_one({"_id": callback.from_user.id})
    # async with httpx.AsyncClient() as client:
    #     page_number = 1
    #     r = await client.get(
    #         f"{settings.FRONT_BASE_URL}/api/v1/site/course/list/?page_size=1&page_number={page_number}")
    #     if r.status_code == 200:
    #         course = r.json()['results'][0]
    #         url = f"{settings.FRONT_BASE_URL}/{user['lang']}/courses/{course['slug']}"
    #         if "discount" in course:
    #             course_price = course['price'] * (1 - course['discount']['percent'] / 100)
    #         else:
    #             course_price = course['price']
    #         caption = _(
    #             """
    #             <b>Kurs nomi:</b> <a href='{href_url}'>{course_title}</a>\n<b>Kurs narxi:</b> {course_price:,} so'm\n\n8-qismga bo'lib to'lash orqali <s>{course_price:,}</s> ga emas atigi {part_price:,} so'mga sotib oling. 🔥
    #             """
    #         ).format(
    #             href_url=url,
    #             course_title=course['translations'][0]['title'],
    #             course_price=int(course_price),
    #             part_price=int(course_price * 1.2 // 8)
    #         )
    #
    #         await self.bot.send_photo(callback.from_user.id,
    #                                   photo=f"{settings.AWS_BUCKET_URL}{course['banner_image']['path']}",
    #                                   caption=caption,
    #                                   reply_markup=get_paginated_course_ikb(),
    #                                   parse_mode="HTML")
    #     await self.get_paginated_courses()
    #
    # async def get_paginated_courses(self, page_number: int = 1, page_size: int = 1):
    #     url = f"{settings.FRONT_BASE_URL}/api/v1/site/course/list/?page_size={page_size}&page_number={page_number}"
    #     print(url)
    #     async with httpx.AsyncClient() as client:
    #         r = await client.get(url)
    #         print(r.json())
