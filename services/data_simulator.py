import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any
from models import Flight, Disruption, DisruptionType
import json
from mongo_utils import mongo_db

class DataSimulator:
    """Simulates real-time operational data for IROPS scenarios"""
    
    def __init__(self):
        # Major US airports with realistic flight patterns
        self.airports = {
            "JFK": {"name": "John F. Kennedy International", "hub": "major", "region": "northeast"},
            "LAX": {"name": "Los Angeles International", "hub": "major", "region": "west"},
            "ORD": {"name": "O'Hare International", "hub": "major", "region": "midwest"},
            "DFW": {"name": "Dallas/Fort Worth International", "hub": "major", "region": "south"},
            "ATL": {"name": "Hartsfield-Jackson Atlanta", "hub": "major", "region": "southeast"},
            "LHR": {"name": "London Heathrow", "hub": "international", "region": "europe"},
            "CDG": {"name": "Charles de Gaulle", "hub": "international", "region": "europe"},
            "NRT": {"name": "Narita International", "hub": "international", "region": "asia"},
            "SIN": {"name": "Singapore Changi", "hub": "international", "region": "asia"},
            "DXB": {"name": "Dubai International", "hub": "international", "region": "middle_east"}
        }
        
        # Realistic aircraft types with capacities
        self.aircraft_types = {
            "B737": {"name": "Boeing 737", "capacity": 180, "range": "domestic"},
            "B787": {"name": "Boeing 787 Dreamliner", "capacity": 250, "range": "international"},
            "A320": {"name": "Airbus A320", "capacity": 160, "range": "domestic"},
            "A350": {"name": "Airbus A350", "capacity": 300, "range": "international"},
            "B777": {"name": "Boeing 777", "capacity": 350, "range": "international"},
            "E190": {"name": "Embraer E190", "capacity": 100, "range": "regional"}
        }
        
        # Realistic disruption scenarios with business impact
        self.disruption_scenarios = {
            "weather": {
                "name": "Severe Weather Event",
                "scenarios": [
                    {
                        "description": "Major thunderstorm system affecting East Coast operations",
                        "affected_airports": ["JFK", "LHR", "CDG"],
                        "severity": "high",
                        "duration_hours": 4,
                        "passenger_impact": "high",
                        "business_impact": "significant"
                    },
                    {
                        "description": "Winter storm with snow and ice affecting Midwest hub",
                        "affected_airports": ["ORD", "DFW"],
                        "severity": "critical",
                        "duration_hours": 6,
                        "passenger_impact": "very_high",
                        "business_impact": "major"
                    }
                ]
            },
            "mechanical": {
                "name": "Aircraft Technical Issues",
                "scenarios": [
                    {
                        "description": "Engine issue on flagship aircraft requiring immediate attention",
                        "affected_airports": ["LAX", "JFK"],
                        "severity": "critical",
                        "duration_hours": 8,
                        "passenger_impact": "high",
                        "business_impact": "major"
                    },
                    {
                        "description": "Hydraulic system malfunction affecting multiple aircraft",
                        "affected_airports": ["ATL", "DFW"],
                        "severity": "high",
                        "duration_hours": 5,
                        "passenger_impact": "medium",
                        "business_impact": "significant"
                    }
                ]
            },
            "crew": {
                "name": "Crew Scheduling Crisis",
                "scenarios": [
                    {
                        "description": "Multiple crew members exceeded duty time limits",
                        "affected_airports": ["ORD", "LAX"],
                        "severity": "high",
                        "duration_hours": 3,
                        "passenger_impact": "medium",
                        "business_impact": "moderate"
                    },
                    {
                        "description": "Unexpected crew illness affecting international operations",
                        "affected_airports": ["LHR", "CDG", "NRT"],
                        "severity": "medium",
                        "duration_hours": 4,
                        "passenger_impact": "high",
                        "business_impact": "significant"
                    }
                ]
            },
            "airport": {
                "name": "Airport Infrastructure Issues",
                "scenarios": [
                    {
                        "description": "Ground equipment failure affecting aircraft servicing",
                        "affected_airports": ["ATL"],
                        "severity": "high",
                        "duration_hours": 2,
                        "passenger_impact": "medium",
                        "business_impact": "moderate"
                    },
                    {
                        "description": "Gate shortage due to unexpected aircraft positioning",
                        "affected_airports": ["JFK", "LAX"],
                        "severity": "medium",
                        "duration_hours": 3,
                        "passenger_impact": "low",
                        "business_impact": "minor"
                    }
                ]
            },
            "traffic": {
                "name": "Air Traffic Control Issues",
                "scenarios": [
                    {
                        "description": "ATC system experiencing technical difficulties",
                        "affected_airports": ["ORD", "DFW", "ATL"],
                        "severity": "critical",
                        "duration_hours": 5,
                        "passenger_impact": "very_high",
                        "business_impact": "major"
                    },
                    {
                        "description": "Airspace congestion due to multiple weather deviations",
                        "affected_airports": ["JFK", "LHR"],
                        "severity": "high",
                        "duration_hours": 3,
                        "passenger_impact": "high",
                        "business_impact": "significant"
                    }
                ]
            }
        }
        
        logging.info("Data simulator initialized with realistic scenarios")
    
    def generate_realistic_flights(self, count: int = 100) -> list:
        """Generate realistic flight data with proper scheduling and passenger loads (MongoDB)"""
        flights = []
        base_time = datetime.utcnow()
        
        # Create flight patterns that make sense
        domestic_routes = [
            ("JFK", "LAX"), ("LAX", "JFK"), ("ORD", "DFW"), ("DFW", "ORD"),
            ("ATL", "JFK"), ("JFK", "ATL"), ("LAX", "ORD"), ("ORD", "LAX"),
            ("DFW", "ATL"), ("ATL", "DFW"), ("JFK", "ORD"), ("ORD", "JFK")
        ]
        
        international_routes = [
            ("JFK", "LHR"), ("LHR", "JFK"), ("LAX", "NRT"), ("NRT", "LAX"),
            ("ORD", "CDG"), ("CDG", "ORD"), ("ATL", "DXB"), ("DXB", "ATL"),
            ("JFK", "SIN"), ("SIN", "JFK"), ("LAX", "LHR"), ("LHR", "LAX")
        ]
        
        all_routes = domestic_routes + international_routes
        
        for i in range(count):
            # Select route
            origin, destination = random.choice(all_routes)
            is_international = (origin, destination) in international_routes
            
            # Generate realistic flight times
            scheduled_departure = base_time + timedelta(
                hours=random.randint(-12, 48),
                minutes=random.randint(0, 59)
            )
            
            # Flight duration based on route
            if is_international:
                flight_duration = timedelta(hours=random.randint(8, 14))
            else:
                flight_duration = timedelta(hours=random.randint(2, 6))
            
            scheduled_arrival = scheduled_departure + flight_duration
            
            # Aircraft selection based on route
            if is_international:
                aircraft_type = random.choice(["B787", "A350", "B777"])
            else:
                aircraft_type = random.choice(["B737", "A320", "E190"])
            
            aircraft_capacity = self.aircraft_types[aircraft_type]["capacity"]
            
            # Realistic passenger count (70-95% capacity)
            passenger_count = int(aircraft_capacity * random.uniform(0.7, 0.95))
            
            # Determine if flight is delayed (20% chance)
            is_delayed = random.random() < 0.2
            delay_minutes = random.randint(15, 180) if is_delayed else 0
            
            # Initialize actual times
            actual_departure = None
            actual_arrival = None
            status = "scheduled"
            
            # Flight status
            if scheduled_departure < base_time:  # Past flights
                if is_delayed:
                    actual_departure = scheduled_departure + timedelta(minutes=delay_minutes)
                    actual_arrival = scheduled_arrival + timedelta(minutes=delay_minutes)
                    status = "delayed" if actual_departure > base_time else "completed"
                else:
                    actual_departure = scheduled_departure + timedelta(minutes=random.randint(-5, 5))
                    actual_arrival = scheduled_arrival + timedelta(minutes=random.randint(-10, 10))
                    status = "completed"
            elif is_delayed and scheduled_departure < base_time + timedelta(hours=2):
                status = "delayed"
            else:
                status = "scheduled"
            
            # Fix disruption_type serialization
            disruption_type = random.choice([d.value for d in DisruptionType]) if is_delayed else None
            flight_doc = {
                'id': i + 1,
                'flight_number': f"AO{100 + i}",
                'origin': origin,
                'destination': destination,
                'scheduled_departure': scheduled_departure.isoformat(),
                'actual_departure': actual_departure.isoformat() if actual_departure else None,
                'scheduled_arrival': scheduled_arrival.isoformat(),
                'actual_arrival': actual_arrival.isoformat() if actual_arrival else None,
                'aircraft_id': f"{aircraft_type}-{random.randint(100, 999)}",
                'crew_list': [f"CREW_{random.randint(1000, 9999)}" for _ in range(random.randint(4, 8))],
                'passenger_count': passenger_count,
                'status': status,
                'delay_minutes': delay_minutes,
                'disruption_type': disruption_type
            }
            flights.append(flight_doc)
        
        return flights
    
    def create_realistic_disruption_scenario(self, scenario_type: str = None) -> dict:
        """Create a realistic disruption scenario with proper business impact (MongoDB)"""
        if not scenario_type:
            scenario_type = random.choice(list(self.disruption_scenarios.keys()))
        scenario_config = random.choice(self.disruption_scenarios[scenario_type]["scenarios"])
        affected_airports = scenario_config["affected_airports"]
        matching_flights = list(mongo_db['flights'].find({
            '$or': [
                {'origin': {'$in': affected_airports}},
                {'destination': {'$in': affected_airports}}
            ],
            'status': 'scheduled'
        }).limit(20))
        affected_flight_count = min(random.randint(3, 8), len(matching_flights))
        affected_flights = random.sample(matching_flights, affected_flight_count) if matching_flights else []
        affected_flight_ids = [f['id'] for f in affected_flights]
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        total_delay_minutes = sum(f.get('delay_minutes', 0) for f in affected_flights)
        disruption_doc = {
            'type': scenario_type,
            'severity': scenario_config["severity"],
            'description': scenario_config["description"],
            'affected_flight_list': affected_flight_ids,
            'affected_airport_list': affected_airports,
            'start_time': datetime.utcnow() - timedelta(minutes=random.randint(5, 60)),
            'estimated_end_time': datetime.utcnow() + timedelta(hours=scenario_config["duration_hours"]),
            'status': "active",
            'total_passengers': total_passengers,
            'total_delay_minutes': total_delay_minutes
        }
        return disruption_doc
    
    def seed_database_with_realistic_scenarios(self):
        """Seed the database with realistic scenarios that demonstrate agent coordination (MongoDB)"""
        logging.info("Seeding database with realistic airline disruption scenarios...")
        # Clear existing data
        mongo_db['agent_communications'].delete_many({})
        mongo_db['disruptions'].delete_many({})
        mongo_db['flights'].delete_many({})
        mongo_db['scenarios'].delete_many({})
        # Generate realistic flights
        logging.info("Generating realistic flight data...")
        flights = self.generate_realistic_flights(120)
        if flights:
            mongo_db['flights'].insert_many(flights)
        logging.info(f"Created {len(flights)} realistic flights")
        # Create disruption scenarios for each type
        logging.info("Creating realistic disruption scenarios...")
        disruption_types = ["weather", "mechanical", "crew", "airport", "traffic"]
        disruptions = []
        for idx, disruption_type in enumerate(disruption_types):
            scenario_config = random.choice(self.disruption_scenarios[disruption_type]["scenarios"])
            affected_airports = scenario_config["affected_airports"]
            matching_flights = list(mongo_db['flights'].find({
                '$or': [
                    {'origin': {'$in': affected_airports}},
                    {'destination': {'$in': affected_airports}}
                ],
                'status': 'scheduled'
            }).limit(20))
            affected_flight_count = min(random.randint(3, 8), len(matching_flights))
            affected_flights = random.sample(matching_flights, affected_flight_count) if matching_flights else []
            affected_flight_ids = [f['id'] for f in affected_flights]
            # Ensure disruption_type is a non-blank string and id is a unique integer
            disruption_doc = {
                'id': idx + 1,
                'type': str(disruption_type) if disruption_type else 'unknown',
                'severity': scenario_config["severity"] or 'unknown',
                'description': scenario_config["description"] or '',
                'affected_flight_list': affected_flight_ids,
                'affected_airport_list': affected_airports,
                'start_time': (datetime.utcnow() - timedelta(minutes=random.randint(5, 60))).isoformat(),
                'estimated_end_time': (datetime.utcnow() + timedelta(hours=scenario_config["duration_hours"])).isoformat(),
                'status': "active",
                'created_at': datetime.utcnow().isoformat()
            }
            mongo_db['disruptions'].insert_one(disruption_doc)
            disruptions.append(disruption_doc)
            logging.info(f"Created {disruption_doc['type']} disruption: {disruption_doc['description']}")
        # Create demo scenarios in Scenario collection
        logging.info("Creating demo scenarios in Scenario collection...")
        scenario_templates = [
            {
                "name": "Severe Weather Disruption",
                "description": "Simulate a major thunderstorm system affecting East Coast operations.",
                "scenario_type": "weather_disruption",
                "parameters": {"severity": "high", "duration": 4, "airports": ["JFK", "LHR", "CDG"]},
                "disruption_id": disruptions[0]['id'] if len(disruptions) > 0 else None
            },
            {
                "name": "Major Mechanical Failure",
                "description": "Test aircraft engine issue requiring immediate attention.",
                "scenario_type": "mechanical_issue",
                "parameters": {"severity": "critical", "duration": 8, "airports": ["LAX", "JFK"]},
                "disruption_id": disruptions[1]['id'] if len(disruptions) > 1 else None
            },
            {
                "name": "Crew Duty Time Crisis",
                "description": "Simulate multiple crew members exceeding duty time limits.",
                "scenario_type": "crew_shortage",
                "parameters": {"severity": "high", "duration": 3, "airports": ["ORD", "LAX"]},
                "disruption_id": disruptions[2]['id'] if len(disruptions) > 2 else None
            },
            {
                "name": "Airport Equipment Failure",
                "description": "Test ground equipment failure affecting aircraft servicing.",
                "scenario_type": "airport_closure",
                "parameters": {"severity": "high", "duration": 2, "airports": ["ATL"]},
                "disruption_id": disruptions[3]['id'] if len(disruptions) > 3 else None
            },
            {
                "name": "ATC System Outage",
                "description": "Simulate air traffic control system experiencing technical difficulties.",
                "scenario_type": "traffic_disruption",
                "parameters": {"severity": "critical", "duration": 5, "airports": ["ORD", "DFW", "ATL"]},
                "disruption_id": disruptions[4]['id'] if len(disruptions) > 4 else None
            }
        ]
        for idx, template in enumerate(scenario_templates):
            scenario_doc = {
                'id': idx + 1,
                'name': template["name"],
                'description': template["description"],
                'scenario_type': template["scenario_type"],
                'parameters': template["parameters"],
                'status': 'completed',
                'created_at': (datetime.utcnow() - timedelta(hours=random.randint(1, 12))).isoformat(),
                'completed_at': (datetime.utcnow() + timedelta(minutes=random.randint(10, 60))).isoformat(),
                'disruption_id': template["disruption_id"]
            }
            mongo_db['scenarios'].insert_one(scenario_doc)
        logging.info("Demo scenarios created in Scenario collection.")
        logging.info("Database seeded successfully with realistic scenarios!")
        return {
            "flights_created": len(flights),
            "disruptions_created": len(disruptions),
            "scenarios_created": len(scenario_templates),
            "scenarios": "Realistic airline disruption scenarios created"
        }
    
    def get_scenario_summary(self) -> Dict[str, Any]:
        """Get a summary of created scenarios for dashboard display (MongoDB)"""
        disruptions = list(mongo_db['disruptions'].find())
        summary = {
            "total_disruptions": len(disruptions),
            "by_type": {},
            "by_severity": {},
            "total_passengers_affected": 0,
            "total_flights_affected": 0
        }
        for disruption in disruptions:
            disruption_type = disruption.get('type', 'unknown')
            summary["by_type"][disruption_type] = summary["by_type"].get(disruption_type, 0) + 1
            severity = disruption.get('severity', 'unknown')
            summary["by_severity"][severity] = summary["by_severity"].get(severity, 0) + 1
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            summary["total_flights_affected"] += len(affected_flights)
            summary["total_passengers_affected"] += sum(f.get('passenger_count', 0) for f in affected_flights)
        return summary
