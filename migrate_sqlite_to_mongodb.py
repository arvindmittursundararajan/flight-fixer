import os
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Flight, Disruption, Agent, AgentCommunication, Scenario
import json
from datetime import datetime

# MongoDB connection
uri = os.getenv('MONGODB_URI', 'YOUR_MONGODB_CONNECTION_STRING_HERE')
client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = client['irops']

# SQLite connection
engine = create_engine('sqlite:///irops.db')
Session = sessionmaker(bind=engine)
session = Session()

def serialize(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if hasattr(obj, 'value'):
        return obj.value
    return obj

def to_dict(obj, exclude=None):
    data = {}
    for col in obj.__table__.columns:
        if exclude and col.name in exclude:
            continue
        val = getattr(obj, col.name)
        if isinstance(val, str):
            # Try to load JSON fields
            try:
                loaded = json.loads(val)
                val = loaded
            except Exception:
                pass
        data[col.name] = serialize(val)
    return data

# Clear existing collections
for name in ['flights', 'disruptions', 'agents', 'agent_communications', 'scenarios']:
    mongo_db[name].delete_many({})

# Migrate Flights
def migrate_flights():
    flights = session.query(Flight).all()
    docs = [to_dict(f) for f in flights]
    if docs:
        mongo_db['flights'].insert_many(docs)
    print(f"Migrated {len(docs)} flights.")

# Migrate Disruptions
def migrate_disruptions():
    disruptions = session.query(Disruption).all()
    docs = [to_dict(d) for d in disruptions]
    if docs:
        mongo_db['disruptions'].insert_many(docs)
    print(f"Migrated {len(docs)} disruptions.")

# Migrate Agents
def migrate_agents():
    agents = session.query(Agent).all()
    docs = [to_dict(a) for a in agents]
    if docs:
        mongo_db['agents'].insert_many(docs)
    print(f"Migrated {len(docs)} agents.")

# Migrate AgentCommunications
def migrate_agent_communications():
    comms = session.query(AgentCommunication).all()
    docs = [to_dict(c) for c in comms]
    if docs:
        mongo_db['agent_communications'].insert_many(docs)
    print(f"Migrated {len(docs)} agent communications.")

# Migrate Scenarios
def migrate_scenarios():
    scenarios = session.query(Scenario).all()
    docs = [to_dict(s) for s in scenarios]
    if docs:
        mongo_db['scenarios'].insert_many(docs)
    print(f"Migrated {len(docs)} scenarios.")

if __name__ == "__main__":
    print("Starting migration from SQLite (irops.db) to MongoDB (irops)...")
    migrate_flights()
    migrate_disruptions()
    migrate_agents()
    migrate_agent_communications()
    migrate_scenarios()
    print("Migration complete!\n")
    # Print summary
    for name in ['flights', 'disruptions', 'agents', 'agent_communications', 'scenarios']:
        count = mongo_db[name].count_documents({})
        print(f"{name}: {count} documents in MongoDB.") 