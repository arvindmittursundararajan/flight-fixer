from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
 
uri = os.getenv('MONGODB_URI', 'YOUR_MONGODB_CONNECTION_STRING_HERE')
client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = client['irops'] 