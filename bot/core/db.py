from motor import motor_asyncio

from bot.core.config import settings

cluster = motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)

# COLLECTION_NAME = 'topskill_study_collection'

database = cluster[settings.MONGODB_DATABASE]
# collections = database[COLLECTION_NAME]
