from .base_agent import BaseAgent
from mongo_utils import mongo_db
from services.gemini_service import GeminiService
from datetime import datetime, timedelta
import logging

class AircraftMaintenanceAgent(BaseAgent):
    """Agent specialized in aircraft maintenance coordination and management"""
    
    def __init__(self):
        super().__init__("Aircraft Maintenance Agent", "aircraft_maintenance")
        self.capabilities = [
            "maintenance_scheduling",
            "aircraft_availability",
            "technical_troubleshooting",
            "spare_parts_management",
            "airworthiness_compliance"
        ]
        self.gemini_service = GeminiService()
    
    def process_disruption(self, disruption_id: int) -> dict:
        """Process disruption for maintenance impact (MongoDB)"""
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            
            # Analyze aircraft impact
            aircraft_analysis = self._analyze_aircraft_impact(affected_flights, disruption)
            
            # Check maintenance requirements
            maintenance_needs = self._assess_maintenance_needs(affected_flights, disruption)
            
            # Find spare aircraft
            spare_aircraft = self._find_spare_aircraft(affected_flights)
            
            # Generate AI-powered maintenance solutions
            ai_solutions = self._get_ai_maintenance_solutions(disruption, aircraft_analysis, maintenance_needs)
            
            # Create maintenance recovery plan
            recovery_plan = self._create_maintenance_recovery_plan(affected_flights, maintenance_needs, spare_aircraft)
            
            result = {
                "success": True,
                "agent": self.name,
                "disruption_id": disruption_id,
                "aircraft_affected": len(aircraft_analysis["affected_aircraft"]),
                "maintenance_required": len(maintenance_needs),
                "spare_aircraft_available": len(spare_aircraft),
                "recovery_plan": recovery_plan,
                "ai_solutions": ai_solutions,
                "estimated_recovery_time": self._estimate_recovery_time(maintenance_needs),
                "airworthiness_status": "Compliant"
            }
            
            # Notify other agents
            self.send_message("Airport Resource Agent", "maintenance_coordination", {
                "disruption_id": disruption_id,
                "hangar_space_needed": len(maintenance_needs),
                "ground_support_required": True
            })
            
            return result
            
        except Exception as e:
            logging.error(f"Aircraft maintenance processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_situation(self, context: dict) -> dict:
        """Analyze aircraft maintenance situation (MongoDB)"""
        try:
            disruption_id = context.get('disruption_id')
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"error": "Disruption not found"}
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': disruption.get('affected_flight_list', [])}}))
            
            analysis = {
                "fleet_impact": self._analyze_fleet_impact(affected_flights),
                "maintenance_urgency": self._assess_maintenance_urgency(disruption),
                "resource_availability": self._assess_maintenance_resources(),
                "spare_aircraft_status": self._check_spare_aircraft_availability(),
                "technical_complexity": self._assess_technical_complexity(disruption)
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Maintenance situation analysis error: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate aircraft maintenance recommendations"""
        recommendations = []
        
        try:
            urgency = analysis.get("maintenance_urgency", "low")
            if urgency == "critical":
                recommendations.append({
                    "priority": "critical",
                    "action": "Deploy emergency maintenance teams immediately",
                    "rationale": "Critical maintenance issues require immediate attention"
                })
            
            fleet_impact = analysis.get("fleet_impact", {})
            if fleet_impact.get("aircraft_out_of_service", 0) > 2:
                recommendations.append({
                    "priority": "high",
                    "action": "Activate spare aircraft from reserves",
                    "rationale": "Multiple aircraft unavailable - utilize backup fleet"
                })
            
            complexity = analysis.get("technical_complexity", "low")
            if complexity == "high":
                recommendations.append({
                    "priority": "medium",
                    "action": "Coordinate with OEM technical support",
                    "rationale": "Complex technical issues may require manufacturer expertise"
                })
            
            recommendations.append({
                "priority": "medium",
                "action": "Monitor parts inventory for expedited ordering",
                "rationale": "Ensure spare parts availability for rapid repairs"
            })
            
        except Exception as e:
            logging.error(f"Maintenance recommendation generation error: {e}")
        
        return recommendations
    
    def _analyze_aircraft_impact(self, affected_flights, disruption):
        """Analyze impact on aircraft from disruption"""
        affected_aircraft = set()
        aircraft_types = {}
        
        for flight in affected_flights:
            if flight.get('aircraft_id'):
                affected_aircraft.add(flight['aircraft_id'])
                aircraft_type = flight['aircraft_id'].split('-')[0]  # Extract type from ID
                aircraft_types[aircraft_type] = aircraft_types.get(aircraft_type, 0) + 1
        
        return {
            "affected_aircraft": list(affected_aircraft),
            "aircraft_count": len(affected_aircraft),
            "aircraft_types": aircraft_types,
            "maintenance_impact": self._determine_maintenance_impact(disruption.get('type', {}).get('value', 'Unknown'))
        }
    
    def _assess_maintenance_needs(self, affected_flights, disruption):
        """Assess maintenance needs based on disruption type"""
        maintenance_needs = []
        
        if disruption.get('type', {}).get('value') == "mechanical":
            # Mechanical disruption requires immediate maintenance
            for flight in affected_flights:
                if flight.get('aircraft_id'):
                    maintenance_needs.append({
                        "aircraft_id": flight['aircraft_id'],
                        "maintenance_type": "unscheduled",
                        "urgency": "critical",
                        "estimated_duration": "4-8 hours",
                        "description": "Mechanical issue investigation and repair",
                        "parts_required": ["TBD - pending diagnosis"],
                        "technicians_required": 3
                    })
        
        elif disruption.get('type', {}).get('value') == "weather":
            # Weather might require inspections
            for flight in affected_flights:
                if flight.get('aircraft_id') and flight.get('delay_minutes') and flight['delay_minutes'] > 180:
                    maintenance_needs.append({
                        "aircraft_id": flight['aircraft_id'],
                        "maintenance_type": "inspection",
                        "urgency": "medium",
                        "estimated_duration": "1-2 hours",
                        "description": "Post-weather event inspection",
                        "parts_required": [],
                        "technicians_required": 1
                    })
        
        return maintenance_needs
    
    def _find_spare_aircraft(self, affected_flights):
        """Find available spare aircraft for substitution"""
        # This would integrate with aircraft management system
        affected_types = set()
        for flight in affected_flights:
            if flight.get('aircraft_id'):
                aircraft_type = flight['aircraft_id'].split('-')[0]
                affected_types.add(aircraft_type)
        
        spare_aircraft = []
        for aircraft_type in affected_types:
            # Simulate spare aircraft availability
            spare_aircraft.extend([
                {
                    "aircraft_id": f"{aircraft_type}-SPARE{i}",
                    "aircraft_type": aircraft_type,
                    "location": "Maintenance Base",
                    "availability": "24 hours",
                    "status": "ready"
                }
                for i in range(1, 3)  # 2 spare aircraft per type
            ])
        
        return spare_aircraft
    
    def _get_ai_maintenance_solutions(self, disruption, aircraft_analysis, maintenance_needs):
        """Get AI-powered maintenance solutions"""
        try:
            context = f"""
            Disruption Type: {disruption.get('type', {}).get('value', 'Unknown')}
            Severity: {disruption.get('severity', 'Unknown')}
            Aircraft Affected: {aircraft_analysis['aircraft_count']}
            Maintenance Tasks: {len(maintenance_needs)}
            """
            
            prompt = f"""
            As an aircraft maintenance specialist, analyze this maintenance disruption:
            
            {context}
            
            Provide solutions for:
            1. Optimal maintenance task prioritization
            2. Resource allocation strategy
            3. Parts procurement approach
            4. Spare aircraft utilization
            5. Schedule recovery optimization
            
            Consider airworthiness requirements and operational constraints.
            Format as actionable maintenance recommendations.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_solutions": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI maintenance solutions error: {e}")
            return {"error": "AI analysis unavailable"}
    
    def _create_maintenance_recovery_plan(self, affected_flights, maintenance_needs, spare_aircraft):
        """Create comprehensive maintenance recovery plan"""
        plan = {
            "immediate_actions": [
                "Assess all aircraft technical status",
                "Deploy maintenance teams to affected aircraft",
                "Coordinate spare aircraft positioning"
            ],
            "maintenance_sequence": [],
            "resource_allocation": {
                "technicians_deployed": sum(need.get("technicians_required", 1) for need in maintenance_needs),
                "spare_aircraft_activated": len(spare_aircraft),
                "hangar_bays_required": min(len(maintenance_needs), 4)
            },
            "timeline": {
                "0-1hr": "Initial assessment and team deployment",
                "1-4hr": "Critical repairs and inspections",
                "4-8hr": "Complete repairs and aircraft return to service"
            }
        }
        
        # Create maintenance sequence
        for i, need in enumerate(maintenance_needs):
            plan["maintenance_sequence"].append({
                "priority": i + 1,
                "aircraft_id": need["aircraft_id"],
                "task": need["description"],
                "estimated_completion": f"{need['estimated_duration']}",
                "assigned_team": f"Team {i + 1}"
            })
        
        return plan
    
    def _estimate_recovery_time(self, maintenance_needs):
        """Estimate total recovery time"""
        if not maintenance_needs:
            return "No maintenance required"
        
        max_duration = 0
        for need in maintenance_needs:
            duration_str = need.get("estimated_duration", "2 hours")
            # Extract hours from duration string
            hours = 2  # Default
            if "4-8" in duration_str:
                hours = 8
            elif "1-2" in duration_str:
                hours = 2
            max_duration = max(max_duration, hours)
        
        return f"{max_duration} hours"
    
    def _determine_maintenance_impact(self, disruption_type):
        """Determine maintenance impact based on disruption type"""
        impact_map = {
            "mechanical": "High - Immediate maintenance required",
            "weather": "Medium - Inspection required",
            "crew": "Low - No maintenance impact",
            "airport": "Low - Possible inspection needed",
            "traffic": "Low - No maintenance impact"
        }
        return impact_map.get(disruption_type, "Unknown")
    
    def _analyze_fleet_impact(self, affected_flights):
        """Analyze impact on fleet availability"""
        aircraft_set = set(f['aircraft_id'] for f in affected_flights if f['aircraft_id'])
        
        return {
            "aircraft_out_of_service": len(aircraft_set),
            "fleet_utilization_impact": f"{len(aircraft_set) * 2}%",  # Rough estimate
            "recovery_priority": "High" if len(aircraft_set) > 3 else "Medium"
        }
    
    def _assess_maintenance_urgency(self, disruption):
        """Assess urgency of maintenance response"""
        if disruption.get('type', {}).get('value') == "mechanical":
            return "critical"
        elif disruption.get('severity', 'Unknown') in ["high", "critical"]:
            return "high"
        else:
            return "medium"
    
    def _assess_maintenance_resources(self):
        """Assess available maintenance resources"""
        return {
            "technicians_available": 12,
            "hangar_capacity": 6,
            "parts_inventory": "Adequate",
            "equipment_availability": "Full"
        }
    
    def _check_spare_aircraft_availability(self):
        """Check spare aircraft availability"""
        return {
            "total_spares": 8,
            "immediately_available": 5,
            "24hr_available": 3,
            "spare_utilization": "65%"
        }
    
    def _assess_technical_complexity(self, disruption):
        """Assess technical complexity of the situation"""
        if disruption.get('type', {}).get('value') == "mechanical" and disruption.get('severity', 'Unknown') == "critical":
            return "high"
        elif disruption.get('type', {}).get('value') == "mechanical":
            return "medium"
        else:
            return "low"
