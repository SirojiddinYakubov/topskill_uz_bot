import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

import aiohttp

from bot.core.config import settings
from bot.core.db import database

COLLECTION_NAME = 'users'

print(13, database)

user_collection = database[COLLECTION_NAME]
print(16, user_collection)


# async def get_access_token() -> str:
#     auth_url = "https://topskill.uz/api/v1/site/auth/jwt/login"
#     data = {
#         "username": settings.TOPSKILL_LOGIN,
#         "password": settings.TOPSKILL_PASSWORD,
#     }
#     access_token = ""
#     async with aiohttp.ClientSession(trust_env=True) as client:
#         async with client.post(auth_url, data=data, ssl=False) as resp:
#             if resp.status == 200:
#                 resp_data = await resp.json()
#                 access_token = resp_data['access_token']
#     return access_token


async def get_user_id(phone: str) -> Optional[UUID]:
    url = f"{settings.BACK_BASE_URL}/api/v1/site/users/get-id-by-phone?phone={phone}"
    async with aiohttp.ClientSession(trust_env=True) as client:
        async with client.get(url, ssl=False) as resp:
            if resp.status == 200:
                resp_data = await resp.json()
                return resp_data
            else:
                logging.error(f"User not found with phone {phone}")


# print(asyncio.run(get_user_id("998919791999")))
# asyncio.run(get_access_token())


async def create_user(_id: int, **kwargs):
    logging.info(f"Inside create_user: _id: {_id}, kwargs: {kwargs}")
    data = {"_id": _id}
    data.update(**kwargs)
    print(data)
    await user_collection.insert_one(data)
    return await user_collection.find_one({"_id": _id})
    # return await user_collection.insert_one({
    #     "_id": _id,
    #     "created_at": str(datetime.now()),
    #     "updated_at": None,
    #     "phone": phone_number,
    #     "status": "active",
    #     "lang": "uz"
    # })


async def update_user(_id: int, **kwargs):
    logging.info(f"Inside update_user: _id: {_id}, kwargs: {kwargs}")

    await user_collection.update_one({"_id": _id}, {"$set": kwargs})

    # print('updated %s document' % result)
    # new_document = await user_collection.find_one({'_id': _id})
    # print('document is now %s' % new_document)
    return await user_collection.find_one({"_id": _id})
