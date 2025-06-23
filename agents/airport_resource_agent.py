from .base_agent import BaseAgent
from mongo_utils import mongo_db
from services.gemini_service import GeminiService
from datetime import datetime, timedelta
import logging

class AirportResourceAgent(BaseAgent):
    """Agent specialized in airport resource coordination and management"""
    
    def __init__(self):
        super().__init__("Airport Resource Agent", "airport_resource")
        self.capabilities = [
            "gate_management",
            "ground_equipment_coordination",
            "terminal_operations",
            "baggage_handling",
            "security_coordination"
        ]
        self.gemini_service = GeminiService()
    
    def process_disruption(self, disruption_id: int) -> dict:
        """Process disruption for airport resource impact (MongoDB)"""
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            
            # Get affected airports
            affected_airports = disruption.get('affected_airport_list', [])
            
            # Analyze resource impact
            resource_analysis = self._analyze_resource_impact(affected_flights, affected_airports)
            
            # Check resource availability
            resource_availability = self._check_resource_availability(affected_airports)
            
            # Assess gate requirements
            gate_requirements = self._assess_gate_requirements(affected_flights)
            
            # Generate AI-powered resource solutions
            ai_solutions = self._get_ai_resource_solutions(disruption, resource_analysis, gate_requirements)
            
            # Create resource allocation plan
            allocation_plan = self._create_resource_allocation_plan(affected_flights, affected_airports, resource_analysis)
            
            result = {
                "success": True,
                "agent": self.name,
                "disruption_id": disruption_id,
                "airports_affected": len(affected_airports),
                "flights_requiring_resources": len(affected_flights),
                "resource_analysis": resource_analysis,
                "gate_requirements": gate_requirements,
                "allocation_plan": allocation_plan,
                "ai_solutions": ai_solutions,
                "estimated_resolution_time": self._estimate_resolution_time(resource_analysis)
            }
            
            # Notify other agents
            self.send_message("Customer Communication Agent", "resource_update", {
                "disruption_id": disruption_id,
                "gate_changes": len(gate_requirements.get("gate_reassignments", [])),
                "service_impacts": resource_analysis.get("service_impacts", [])
            })
            
            return result
            
        except Exception as e:
            logging.error(f"Airport resource processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_situation(self, context: dict) -> dict:
        """Analyze airport resource situation (MongoDB)"""
        try:
            disruption_id = context.get('disruption_id')
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"error": "Disruption not found"}
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': disruption.get('affected_flight_list', [])}}))
            
            # Get affected airports
            affected_airports = disruption.get('affected_airport_list', [])
            
            analysis = {
                "capacity_impact": self._analyze_capacity_impact(affected_airports),
                "resource_strain": self._assess_resource_strain(affected_flights, affected_airports),
                "operational_bottlenecks": self._identify_bottlenecks(affected_flights, affected_airports),
                "passenger_flow_impact": self._assess_passenger_flow_impact(affected_flights),
                "equipment_availability": self._check_equipment_status(affected_airports)
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Airport resource situation analysis error: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate airport resource recommendations"""
        recommendations = []
        
        try:
            capacity_impact = analysis.get("capacity_impact", {})
            if capacity_impact.get("congestion_level", "low") == "high":
                recommendations.append({
                    "priority": "critical",
                    "action": "Activate overflow gate areas and remote stands",
                    "rationale": "High airport congestion requires additional capacity"
                })
            
            resource_strain = analysis.get("resource_strain", {})
            if resource_strain.get("ground_equipment_utilization", 0) > 90:
                recommendations.append({
                    "priority": "high",
                    "action": "Deploy backup ground support equipment",
                    "rationale": "Ground equipment at capacity - risk of service delays"
                })
            
            bottlenecks = analysis.get("operational_bottlenecks", [])
            if "baggage_handling" in bottlenecks:
                recommendations.append({
                    "priority": "medium",
                    "action": "Increase baggage handling staff and equipment",
                    "rationale": "Baggage system bottleneck identified"
                })
            
            passenger_flow = analysis.get("passenger_flow_impact", {})
            if passenger_flow.get("terminal_congestion", "normal") == "high":
                recommendations.append({
                    "priority": "medium",
                    "action": "Implement crowd control measures in terminals",
                    "rationale": "High passenger volume requires flow management"
                })
            
        except Exception as e:
            logging.error(f"Airport resource recommendation generation error: {e}")
        
        return recommendations
    
    def _analyze_resource_impact(self, affected_flights, affected_airports):
        """Analyze impact on airport resources"""
        analysis = {
            "gates_needed": len(affected_flights),
            "ground_equipment_demand": self._calculate_equipment_demand(affected_flights),
            "passenger_processing_load": sum(f.get('passenger_count', 0) for f in affected_flights),
            "baggage_handling_impact": self._assess_baggage_impact(affected_flights),
            "service_impacts": []
        }
        
        # Identify service impacts
        if len(affected_flights) > 10:
            analysis["service_impacts"].append("High passenger volume - expect longer wait times")
        
        if any(f.get('delay_minutes', 0) and f.get('delay_minutes', 0) > 120 for f in affected_flights):
            analysis["service_impacts"].append("Extended delays - passenger services required")
        
        return analysis
    
    def _check_resource_availability(self, affected_airports):
        """Check availability of airport resources"""
        availability = {}
        
        for airport in affected_airports:
            # This would integrate with airport management systems
            availability[airport] = {
                "gates_available": 8,  # Simulated data
                "remote_stands": 12,
                "ground_equipment": {
                    "pushback_tugs": 6,
                    "belt_loaders": 8,
                    "catering_trucks": 4,
                    "fuel_trucks": 3
                },
                "personnel": {
                    "ground_handlers": 15,
                    "customer_service": 8,
                    "baggage_handlers": 12
                },
                "terminal_capacity": "Normal"
            }
        
        return availability
    
    def _assess_gate_requirements(self, affected_flights):
        """Assess gate assignment requirements"""
        gate_requirements = {
            "total_gates_needed": len(affected_flights),
            "gate_reassignments": [],
            "remote_stand_usage": 0,
            "gate_conflicts": []
        }
        
        # Simulate gate assignments
        for i, flight in enumerate(affected_flights[:5]):  # First 5 flights
            gate_requirements["gate_reassignments"].append({
                "flight_number": flight.get('flight_number', ''),
                "original_gate": f"{flight.get('origin', '')}-{10 + i}",
                "new_gate": f"{flight.get('origin', '')}-{20 + i}",
                "reason": "Disruption accommodation"
            })
        
        # Some flights may need remote stands
        if len(affected_flights) > 10:
            gate_requirements["remote_stand_usage"] = len(affected_flights) - 10
        
        return gate_requirements
    
    def _get_ai_resource_solutions(self, disruption, resource_analysis, gate_requirements):
        """Get AI-powered airport resource solutions"""
        try:
            context = f"""
            Disruption: {disruption.get('type', '')} - {disruption.get('severity', '')}
            Airports Affected: {len(disruption.get('affected_airport_list', []))}
            Gates Needed: {gate_requirements['total_gates_needed']}
            Passenger Load: {resource_analysis['passenger_processing_load']}
            """
            
            prompt = f"""
            As an airport operations specialist, analyze this resource disruption:
            
            {context}
            
            Provide solutions for:
            1. Optimal gate allocation strategy
            2. Ground equipment deployment
            3. Passenger flow management
            4. Terminal operations coordination
            5. Service level maintenance
            
            Consider operational constraints and passenger experience.
            Format as actionable resource management recommendations.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_solutions": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI resource solutions error: {e}")
            return {"error": "AI analysis unavailable"}
    
    def _create_resource_allocation_plan(self, affected_flights, affected_airports, resource_analysis):
        """Create comprehensive resource allocation plan"""
        plan = {
            "gate_assignments": [],
            "equipment_deployment": {},
            "staffing_adjustments": {},
            "passenger_services": [],
            "timeline": {
                "immediate": "Secure gates and deploy basic equipment",
                "30min": "Complete equipment positioning and staff briefing",
                "60min": "Full service restoration with passenger accommodation"
            }
        }
        
        # Gate assignments
        for i, flight in enumerate(affected_flights[:10]):  # Limit to manageable number
            plan["gate_assignments"].append({
                "flight": flight.get('flight_number', ''),
                "gate": f"Gate {i + 1}",
                "equipment_assigned": ["Pushback tug", "Belt loader", "Ground power"],
                "service_level": "Full service"
            })
        
        # Equipment deployment by airport
        for airport in affected_airports:
            plan["equipment_deployment"][airport] = {
                "additional_tugs": 2,
                "extra_belt_loaders": 3,
                "backup_ground_power": 2,
                "catering_support": 1
            }
        
        # Staffing adjustments
        for airport in affected_airports:
            plan["staffing_adjustments"][airport] = {
                "additional_ground_crew": 5,
                "extra_customer_service": 3,
                "baggage_handling_boost": 4,
                "shift_extensions": "2 hours"
            }
        
        # Passenger services
        if resource_analysis["passenger_processing_load"] > 500:
            plan["passenger_services"] = [
                "Mobile check-in assistance",
                "Additional customer service desks",
                "Refreshment stations for delayed passengers",
                "Enhanced boarding announcements"
            ]
        
        return plan
    
    def _estimate_resolution_time(self, resource_analysis):
        """Estimate time to restore normal operations"""
        base_time = 60  # Base 1 hour
        
        # Add time based on complexity
        if resource_analysis["gates_needed"] > 10:
            base_time += 30
        
        if resource_analysis["passenger_processing_load"] > 1000:
            base_time += 30
        
        if resource_analysis["service_impacts"]:
            base_time += 15 * len(resource_analysis["service_impacts"])
        
        return f"{base_time} minutes"
    
    def _calculate_equipment_demand(self, affected_flights):
        """Calculate ground equipment demand"""
        return {
            "pushback_tugs": len(affected_flights),
            "belt_loaders": len(affected_flights) * 2,  # 2 per flight
            "catering_trucks": len(affected_flights),
            "fuel_trucks": max(len(affected_flights) // 2, 1),
            "ground_power_units": len(affected_flights)
        }
    
    def _assess_baggage_impact(self, affected_flights):
        """Assess impact on baggage handling"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        
        return {
            "estimated_bags": total_passengers * 1.5,  # Average bags per passenger
            "additional_screening_time": "30 minutes",
            "baggage_claim_impact": "Extended wait times expected",
            "staffing_increase_needed": max(total_passengers // 100, 2)
        }
    
    def _analyze_capacity_impact(self, affected_airports):
        """Analyze impact on airport capacity"""
        return {
            "congestion_level": "high" if len(affected_airports) > 2 else "medium",
            "gate_utilization": "85%",
            "runway_impact": "Minimal",
            "terminal_impact": "Moderate"
        }
    
    def _assess_resource_strain(self, affected_flights, affected_airports):
        """Assess strain on airport resources"""
        return {
            "ground_equipment_utilization": 85,
            "staffing_utilization": 90,
            "gate_utilization": 80,
            "critical_resources": ["Ground crew", "Customer service staff"]
        }
    
    def _identify_bottlenecks(self, affected_flights, affected_airports):
        """Identify operational bottlenecks"""
        bottlenecks = []
        
        if len(affected_flights) > 15:
            bottlenecks.append("gate_availability")
        
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        if total_passengers > 1000:
            bottlenecks.extend(["security_checkpoint", "baggage_handling"])
        
        if len(affected_airports) > 3:
            bottlenecks.append("coordination_complexity")
        
        return bottlenecks
    
    def _assess_passenger_flow_impact(self, affected_flights):
        """Assess impact on passenger flow"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        
        return {
            "terminal_congestion": "high" if total_passengers > 800 else "medium",
            "check_in_impact": "Extended wait times",
            "security_impact": "Possible delays",
            "boarding_impact": "Gate congestion likely"
        }
    
    def _check_equipment_status(self, affected_airports):
        """Check status of ground equipment"""
        status = {}
        
        for airport in affected_airports:
            status[airport] = {
                "operational_equipment": "95%",
                "backup_availability": "Good",
                "maintenance_status": "Normal",
                "critical_spares": "Available"
            }
        
        return status
