import logging
from abc import abstractmethod
from typing import Optional
from uuid import UUID

from bot.core.config import settings
from bot.core.db import database
from bot.providers.sms_providers.eskiz_sms.async_ import EskizSMS

from bot.providers.sms_providers.eskiz_sms.types import Response


class BaseSmsClient:
    @classmethod
    async def create_obj(cls,
                         count: int,
                         message: str,
                         phone: str,
                         created_by_id: int):
        COLLECTION_NAME = 'sent_sms'
        sms_collection = database[COLLECTION_NAME]

        await sms_collection.insert_one({
            "created_by_id": created_by_id,
            "message": message,
            "phone": phone,
            "count": count
        })
        return

    @abstractmethod
    async def send_sms(self, phone: str, message: str, created_by_id: int) -> Response:
        raise NotImplementedError


class EskizSmsClient(BaseSmsClient):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    async def send_sms(self, phone: str, message: str,
                       created_by_id: int) -> Response:
        eskiz = EskizSMS(self.email, self.password)
        response = await eskiz.send_sms(phone, message, from_whom='4546', callback_url=None)
        count = eskiz.count_sms_chars(message)
        await self.create_obj(count, message, phone, created_by_id)
        return response


def eskiz_auth() -> EskizSmsClient:
    sms_client = EskizSmsClient(
        email=settings.ESKIZ_EMAIL,
        password=settings.ESKIZ_PASSWORD
    )
    return sms_client
