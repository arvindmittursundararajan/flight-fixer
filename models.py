# All SQLAlchemy model classes removed. Use mongo_db collections directly in codebase.
# If you need schema validation, use Pydantic or plain dicts.

from datetime import datetime
from enum import Enum
import json

class DisruptionType(Enum):
    WEATHER = "weather"
    MECHANICAL = "mechanical"
    CREW = "crew" 
    AIRPORT = "airport"
    TRAFFIC = "traffic"

class AgentStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    PROCESSING = "processing"
    ERROR = "error"

class AgentType(Enum):
    PASSENGER_REBOOKING = "passenger_rebooking"
    CREW_SCHEDULING = "crew_scheduling"
    AIRCRAFT_MAINTENANCE = "aircraft_maintenance"
    AIRPORT_RESOURCE = "airport_resource"
    CUSTOMER_COMMUNICATION = "customer_communication"

class Flight:
    __tablename__ = 'flights'
    
    id = None
    flight_number = None
    origin = None
    destination = None
    scheduled_departure = None
    actual_departure = None
    scheduled_arrival = None
    actual_arrival = None
    aircraft_id = None
    crew_ids = None
    passenger_count = None
    status = None
    delay_minutes = None
    disruption_type = None
    created_at = None
    updated_at = None
    
    def __repr__(self):
        return f'<Flight {self.flight_number}: {self.origin}->{self.destination}>'
    
    @property
    def crew_list(self):
        if self.crew_ids:
            try:
                return json.loads(self.crew_ids)
            except:
                return []
        return []
    
    @crew_list.setter
    def crew_list(self, value):
        self.crew_ids = json.dumps(value) if value else None

class Disruption:
    __tablename__ = 'disruptions'
    
    id = None
    type = None
    severity = None
    description = None
    affected_flights = None
    affected_airports = None
    start_time = None
    end_time = None
    estimated_end_time = None
    status = None
    created_at = None
    updated_at = None
    
    def __repr__(self):
        return f'<Disruption {self.id}: {self.type.value} - {self.severity}>'
    
    @property
    def affected_flight_list(self):
        if self.affected_flights:
            try:
                return json.loads(self.affected_flights)
            except:
                return []
        return []
    
    @affected_flight_list.setter
    def affected_flight_list(self, value):
        self.affected_flights = json.dumps(value) if value else None
    
    @property
    def affected_airport_list(self):
        if self.affected_airports:
            try:
                return json.loads(self.affected_airports)
            except:
                return []
        return []
    
    @affected_airport_list.setter
    def affected_airport_list(self, value):
        self.affected_airports = json.dumps(value) if value else None

class Agent:
    __tablename__ = 'agents'
    
    id = None
    name = None
    type = None
    status = None
    current_task = None
    capabilities = None
    last_activity = None
    created_at = None
    
    def __repr__(self):
        return f'<Agent {self.name}: {self.type.value}>'

class AgentCommunication:
    __tablename__ = 'agent_communications'
    
    id = None
    sender = None
    receiver = None
    message_type = None
    content = None
    processed = None
    timestamp = None
    disruption_id = None
    
    def __repr__(self):
        return f'<Communication {self.sender}->{self.receiver}: {self.message_type}>'
        
    @property
    def content_dict(self):
        try:
            return json.loads(self.content)
        except:
            return {}
    
    @content_dict.setter
    def content_dict(self, value):
        self.content = json.dumps(value) if value else "{}"

class Scenario:
    __tablename__ = 'scenarios'
    
    id = None
    name = None
    description = None
    scenario_type = None
    parameters = None
    results = None
    status = None
    created_at = None
    completed_at = None
    
    def __repr__(self):
        return f'<Scenario {self.name}: {self.scenario_type}>'
