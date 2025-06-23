from .base_agent import BaseAgent
from mongo_utils import mongo_db
from services.gemini_service import GeminiService
from datetime import datetime, timedelta
import logging

class PassengerRebookingAgent(BaseAgent):
    """Agent specialized in passenger rebooking and accommodation"""
    
    def __init__(self):
        super().__init__("Passenger Rebooking Agent", "passenger_rebooking")
        self.capabilities = [
            "alternative_flight_search",
            "passenger_accommodation",
            "rebooking_optimization",
            "passenger_prioritization",
            "cost_analysis"
        ]
        self.gemini_service = GeminiService()
    
    def process_disruption(self, disruption_id: int) -> dict:
        """Process disruption for passenger rebooking (MongoDB)"""
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            
            # Get context from other agents
            crew_messages = self._get_disruption_messages(disruption_id, sender_name="crew_scheduling")
            crew_context = crew_messages[0] if crew_messages else {}
            
            # Get affected flights
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            
            # Analyze passenger impact
            total_passengers = sum(flight.get('passenger_count', 0) for flight in affected_flights)
            
            # Find alternative flights
            alternatives = self._find_alternative_flights(affected_flights)
            
            # Generate AI-powered recommendations
            ai_analysis = self._get_ai_recommendations(disruption, affected_flights, alternatives, crew_context)
            
            # Create rebooking plan
            rebooking_plan = self._create_rebooking_plan(affected_flights, alternatives, ai_analysis)
            
            result = {
                "success": True,
                "agent": self.name,
                "disruption_id": disruption_id,
                "passengers_affected": total_passengers,
                "flights_affected": len(affected_flights),
                "alternatives_found": len(alternatives),
                "rebooking_plan": rebooking_plan,
                "ai_recommendations": ai_analysis,
                "estimated_rebooking_time": "2-4 hours",
                "priority_passengers": self._identify_priority_passengers(affected_flights),
                "crew_context": crew_context
            }
            
            # Send updates to other agents
            self.send_message("Customer Communication Agent", "passenger_update", {
                "disruption_id": disruption_id,
                "passengers_affected": total_passengers,
                "rebooking_status": "in_progress"
            })
            
            return result
            
        except Exception as e:
            logging.error(f"Passenger rebooking processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_situation(self, context: dict) -> dict:
        """Analyze passenger rebooking situation (MongoDB)"""
        try:
            disruption_id = context.get('disruption_id')
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            
            if not disruption:
                return {"error": "Disruption not found"}
            
            # Get affected flights and passengers
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': disruption.get('affected_flight_list', [])}}))
            
            analysis = {
                "passenger_impact": {
                    "total_affected": sum(f.get('passenger_count', 0) for f in affected_flights),
                    "connecting_passengers": self._count_connecting_passengers(affected_flights),
                    "priority_passengers": len(self._identify_priority_passengers(affected_flights))
                },
                "rebooking_complexity": self._assess_rebooking_complexity(affected_flights),
                "time_sensitivity": self._assess_time_sensitivity(affected_flights),
                "available_capacity": self._check_available_capacity(affected_flights)
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Situation analysis error: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate passenger rebooking recommendations"""
        recommendations = []
        
        try:
            if analysis.get("passenger_impact", {}).get("total_affected", 0) > 100:
                recommendations.append({
                    "priority": "high",
                    "action": "Activate emergency rebooking protocols",
                    "rationale": "Large number of passengers affected"
                })
            
            if analysis.get("rebooking_complexity") == "high":
                recommendations.append({
                    "priority": "medium",
                    "action": "Request additional rebooking staff",
                    "rationale": "Complex rebooking scenarios require extra resources"
                })
            
            if analysis.get("time_sensitivity") == "critical":
                recommendations.append({
                    "priority": "critical",
                    "action": "Prioritize same-day rebooking options",
                    "rationale": "Time-critical passengers need immediate alternatives"
                })
            
            recommendations.append({
                "priority": "medium",
                "action": "Coordinate with partner airlines for additional capacity",
                "rationale": "Maximize rebooking options"
            })
            
        except Exception as e:
            logging.error(f"Recommendation generation error: {e}")
        
        return recommendations
    
    def _find_alternative_flights(self, affected_flights):
        """Find alternative flights for rebooking"""
        alternatives = []
        
        for flight in affected_flights:
            # Look for flights on same route within next 24 hours
            alternative_flights = list(mongo_db['flights'].find({
                'origin': flight.get('origin', ''),
                'destination': flight.get('destination', ''),
                'scheduled_departure': {'$gte': flight.get('scheduled_departure', 0)},
                'scheduled_departure': {'$lte': flight.get('scheduled_departure', 0) + 86400},
                'status': 'scheduled',
                'id': {'$ne': flight.get('id', '')}
            }).limit(5))
            
            for alt_flight in alternative_flights:
                alternatives.append({
                    "original_flight": flight.get('flight_number', ''),
                    "alternative_flight": alt_flight.get('flight_number', ''),
                    "departure_time": alt_flight.get('scheduled_departure', ''),
                    "delay_from_original": int((alt_flight.get('scheduled_departure', 0) - flight.get('scheduled_departure', 0)) / 60)
                })
        
        return alternatives
    
    def _get_ai_recommendations(self, disruption, affected_flights, alternatives, crew_context):
        """Get AI-powered rebooking recommendations"""
        try:
            context = f"""
            Disruption: {disruption.get('type', 'Unknown')} - {disruption.get('severity', 'Unknown')}
            Description: {disruption.get('description', 'No description available')}
            Affected Flights: {len(affected_flights)}
            Total Passengers: {sum(f.get('passenger_count', 0) for f in affected_flights)}
            Available Alternatives: {len(alternatives)}
            Crew Availability Status: {crew_context.get('status', 'Unknown')}
            Crews Reassigned: {crew_context.get('crews_reassigned', 'N/A')}
            """
            
            prompt = f"""
            As an airline passenger rebooking specialist, analyze this disruption situation:
            
            {context}
            
            Provide recommendations for:
            1. Passenger prioritization strategy
            2. Rebooking sequence optimization
            3. Customer communication approach
            4. Compensation considerations
            
            Format as JSON with clear actionable recommendations.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_analysis": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI recommendation error: {e}")
            return {"error": "AI analysis unavailable"}
    
    def _create_rebooking_plan(self, affected_flights, alternatives, ai_analysis):
        """Create comprehensive rebooking plan"""
        plan = {
            "phases": [
                {
                    "phase": "Priority Passengers",
                    "duration": "30 minutes",
                    "actions": ["Process elite status passengers", "Handle special needs passengers"]
                },
                {
                    "phase": "Connecting Passengers", 
                    "duration": "60 minutes",
                    "actions": ["Rebook tight connections", "Coordinate with hub operations"]
                },
                {
                    "phase": "General Passengers",
                    "duration": "120 minutes", 
                    "actions": ["Process remaining passengers", "Offer accommodation if needed"]
                }
            ],
            "resources_needed": {
                "staff": 8,
                "workstations": 6,
                "phone_lines": 12
            },
            "estimated_completion": "3-4 hours"
        }
        
        return plan
    
    def _identify_priority_passengers(self, affected_flights):
        """Identify passengers requiring priority handling"""
        # This would integrate with passenger management system
        priority_categories = [
            "Elite status members",
            "Unaccompanied minors", 
            "Passengers with special needs",
            "Tight connections",
            "Medical emergencies"
        ]
        
        return priority_categories
    
    def _count_connecting_passengers(self, affected_flights):
        """Estimate connecting passengers (would integrate with PNR system)"""
        return sum(int((flight.get('passenger_count', 0) or 0) * 0.3) for flight in affected_flights)
    
    def _assess_rebooking_complexity(self, affected_flights):
        """Assess complexity of rebooking operation"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        
        if total_passengers > 500:
            return "high"
        elif total_passengers > 200:
            return "medium" 
        else:
            return "low"
    
    def _assess_time_sensitivity(self, affected_flights):
        """Assess time sensitivity of rebooking"""
        now = datetime.utcnow()
        urgent_flights = [f for f in affected_flights 
                         if f.get('scheduled_departure', 0) <= now.timestamp()]
        
        if len(urgent_flights) > len(affected_flights) * 0.5:
            return "critical"
        elif len(urgent_flights) > 0:
            return "high"
        else:
            return "medium"
    
    def _check_available_capacity(self, affected_flights):
        """Check available capacity on alternative flights"""
        # This would integrate with inventory management system
        return {
            "same_day_availability": "Limited",
            "next_day_availability": "Good", 
            "partner_airline_options": "Available"
        }
