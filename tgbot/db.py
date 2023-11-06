import pymongo

from tgbot.config import config

client = pymongo.MongoClient(config.db.mongo_url)
db = client['test']
collection = db['sample_collection']
