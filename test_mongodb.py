from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = os.getenv('MONGODB_URI', 'YOUR_MONGODB_CONNECTION_STRING_HERE')
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Ping failed:", e)
    exit(1)

# Create/use a sample database and collection
sample_db = client['flightops_test']
sample_collection = sample_db['sample_collection']

# Insert a sample document
sample_doc = {"flight": "AO123", "status": "on_time", "passengers": 180}
insert_result = sample_collection.insert_one(sample_doc)
print(f"Inserted document with _id: {insert_result.inserted_id}")

# Read back the document
found_doc = sample_collection.find_one({"_id": insert_result.inserted_id})
print("Read back document:", found_doc)

# Clean up: delete the test document and collection (optional)
sample_collection.delete_one({"_id": insert_result.inserted_id})
print("Test document deleted. Test complete.") 