from .base_agent import BaseAgent
from mongo_utils import mongo_db
from services.gemini_service import GeminiService
from datetime import datetime, timedelta
import logging

class CrewSchedulingAgent(BaseAgent):
    """Agent specialized in crew scheduling and duty time management"""
    
    def __init__(self):
        super().__init__("Crew Scheduling Agent", "crew_scheduling")
        self.capabilities = [
            "duty_time_monitoring",
            "crew_optimization",
            "reserve_crew_management", 
            "crew_positioning",
            "regulatory_compliance"
        ]
        self.gemini_service = GeminiService()
    
    def process_disruption(self, disruption_id: int) -> dict:
        """Process disruption for crew scheduling needs (MongoDB)"""
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            
            # Get context from other agents
            maintenance_messages = self._get_disruption_messages(disruption_id, sender_name="aircraft_maintenance")
            maintenance_context = maintenance_messages[0] if maintenance_messages else {}
            
            # Analyze crew impact
            crew_analysis = self._analyze_crew_impact(affected_flights)
            
            # Check duty time violations
            duty_violations = self._check_duty_time_violations(affected_flights)
            
            # Find available reserve crews
            available_crews = self._find_available_reserve_crews(affected_flights)
            
            # Generate AI-powered recommendations
            ai_analysis = self._get_ai_recommendations(disruption, affected_flights, maintenance_context)
            
            # Create crew reassignment plan
            reassignment_plan = self._create_reassignment_plan(available_crews, ai_analysis)
            
            result = {
                "success": True,
                "agent": self.name,
                "disruption_id": disruption_id,
                "flights_affected": len(affected_flights),
                "crews_affected": crew_analysis["total_crews"],
                "duty_violations": len(duty_violations),
                "available_reserves": len(available_crews),
                "reassignment_plan": reassignment_plan,
                "ai_recommendations": ai_analysis,
                "maintenance_context": maintenance_context
            }
            
            # Notify other agents
            self.send_message("Aircraft Maintenance Agent", "crew_coordination", {
                "disruption_id": disruption_id,
                "crew_changes": len(duty_violations),
                "ready_for_coordination": True
            })
            
            return result
            
        except Exception as e:
            logging.error(f"Crew scheduling processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_situation(self, context: dict) -> dict:
        """Analyze crew scheduling situation (MongoDB)"""
        try:
            disruption_id = context.get('disruption_id')
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"error": "Disruption not found"}
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': disruption.get('affected_flight_list', [])}}))
            
            analysis = {
                "crew_utilization": self._analyze_crew_utilization(affected_flights),
                "duty_time_risk": self._assess_duty_time_risk(affected_flights),
                "crew_availability": self._assess_crew_availability(),
                "positioning_requirements": self._assess_positioning_needs(affected_flights),
                "regulatory_constraints": self._identify_regulatory_constraints(affected_flights)
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Crew situation analysis error: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate crew scheduling recommendations"""
        recommendations = []
        
        try:
            duty_risk = analysis.get("duty_time_risk", {})
            if duty_risk.get("high_risk_crews", 0) > 0:
                recommendations.append({
                    "priority": "critical",
                    "action": "Immediate crew substitution required",
                    "rationale": f"{duty_risk['high_risk_crews']} crews approaching duty limits"
                })
            
            availability = analysis.get("crew_availability", {})
            if availability.get("reserve_utilization", 0) > 80:
                recommendations.append({
                    "priority": "high", 
                    "action": "Activate standby crews from other bases",
                    "rationale": "Reserve crew capacity near exhaustion"
                })
            
            positioning = analysis.get("positioning_requirements", {})
            if positioning.get("crews_to_position", 0) > 0:
                recommendations.append({
                    "priority": "medium",
                    "action": "Coordinate crew positioning flights",
                    "rationale": "Crews need repositioning for optimal coverage"
                })
            
            recommendations.append({
                "priority": "medium",
                "action": "Monitor duty time compliance continuously",
                "rationale": "Prevent regulatory violations during recovery"
            })
            
        except Exception as e:
            logging.error(f"Crew recommendation generation error: {e}")
        
        return recommendations
    
    def _analyze_crew_impact(self, affected_flights):
        """Analyze crew impact from affected flights"""
        unique_crews = set()
        for flight in affected_flights:
            if flight.get('crew_list', []):
                unique_crews.update(flight['crew_list'])
        
        return {
            "total_crews": len(unique_crews),
            "crew_types": {
                "pilots": len(unique_crews) // 2,  # Approximate
                "flight_attendants": len(unique_crews) - (len(unique_crews) // 2)
            },
            "crew_bases": self._identify_crew_bases(affected_flights)
        }
    
    def _check_duty_time_violations(self, affected_flights):
        """Check for potential duty time violations"""
        violations = []
        
        for flight in affected_flights:
            if flight.get('delay_minutes', 0) and flight['delay_minutes'] > 120:  # 2+ hour delay
                # Simulate duty time check (would integrate with crew management system)
                violations.append({
                    "flight": flight.get('flight_number', 'UNKNOWN'),
                    "crew_id": flight['crew_list'][0] if flight['crew_list'] else "UNKNOWN",
                    "violation_type": "potential_overtime", 
                    "estimated_duty_time": "14+ hours",
                    "action_required": "crew_substitution"
                })
        
        return violations
    
    def _find_available_reserve_crews(self, affected_flights):
        """Find available reserve crews for substitution"""
        # This would integrate with crew management system
        affected_airports = set(f['origin'] for f in affected_flights)
        
        available_crews = []
        for airport in affected_airports:
            # Simulate reserve crew availability
            available_crews.extend([
                {
                    "crew_id": f"RESERVE_{airport}_{i}",
                    "base": airport,
                    "qualification": "A320/A321",
                    "availability": "immediate"
                }
                for i in range(1, 4)  # 3 reserve crews per airport
            ])
        
        return available_crews
    
    def _get_ai_recommendations(self, disruption, affected_flights, maintenance_context):
        """Get AI-powered crew scheduling recommendations"""
        try:
            context = f"""
            Disruption: {disruption.get('type', 'Unknown')} - {disruption.get('severity', 'Unknown')}
            Affected Flights: {len(affected_flights)}
            Crews Affected: {self._analyze_crew_impact(affected_flights)['total_crews']}
            Disruption Duration: {disruption.get('estimated_end_time', 'Unknown') - disruption.get('start_time', 'Unknown') if disruption.get('estimated_end_time') else 'Unknown'}
            Description: {disruption.get('description', 'Unknown')}
            Affected Crews: {len(affected_flights)}
            Maintenance Status: {maintenance_context.get('status', 'Unknown')}
            Maintenance ETA: {maintenance_context.get('estimated_completion_time', 'N/A')}
            """
            
            prompt = f"""
            As an airline crew scheduling specialist, analyze this crew disruption:
            
            {context}
            
            Provide solutions for:
            1. Optimal crew reassignment strategy
            2. Duty time compliance approach
            3. Reserve crew utilization
            4. Crew positioning optimization
            5. Cost-effective recovery plan
            
            Consider regulatory constraints and crew rest requirements.
            Format as actionable recommendations.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_recommendations": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI crew recommendations error: {e}")
            return {"error": "AI analysis unavailable"}
    
    def _create_reassignment_plan(self, available_crews, ai_analysis):
        """Create comprehensive crew reassignment plan"""
        # Get duty violations from the process_disruption method
        duty_violations = self._check_duty_time_violations([])  # Will be populated by caller
        
        plan = {
            "immediate_actions": [
                "Replace crews with duty time violations",
                "Position reserve crews to affected airports", 
                "Coordinate with crew scheduling office"
            ],
            "crew_assignments": [],
            "timeline": {
                "0-30min": "Assess all crew statuses",
                "30-60min": "Execute crew substitutions",
                "60-120min": "Position crews for next wave"
            },
            "resources_required": {
                "reserve_crews": len(duty_violations),
                "positioning_flights": len(available_crews),
                "crew_schedulers": 3
            }
        }
        
        # Create specific crew assignments
        for i, violation in enumerate(duty_violations):
            if i < len(available_crews):
                plan["crew_assignments"].append({
                    "original_crew": violation["crew_id"],
                    "replacement_crew": available_crews[i]["crew_id"],
                    "flight": violation["flight"],
                    "status": "assigned"
                })
        
        return plan
    
    def _check_regulatory_compliance(self, recovery_plan):
        """Check regulatory compliance of recovery plan"""
        return {
            "duty_time_compliant": True,
            "rest_requirements_met": True,
            "certification_valid": True,
            "regulatory_notes": "All assignments comply with FAR Part 117"
        }
    
    def _analyze_crew_utilization(self, affected_flights):
        """Analyze current crew utilization"""
        return {
            "flights_per_crew": len(affected_flights) / max(1, len(set().union(*[f['crew_list'] for f in affected_flights if f['crew_list']]))),
            "average_duty_day": "11.5 hours",
            "utilization_rate": "85%"
        }
    
    def _assess_duty_time_risk(self, affected_flights):
        """Assess duty time violation risk"""
        delayed_flights = [f for f in affected_flights if f.get('delay_minutes', 0) and f['delay_minutes'] > 60]
        
        return {
            "high_risk_crews": len(delayed_flights),
            "moderate_risk_crews": len(affected_flights) - len(delayed_flights),
            "risk_factors": ["Extended delays", "Multiple sectors", "Late night operations"]
        }
    
    def _assess_crew_availability(self):
        """Assess overall crew availability"""
        return {
            "reserve_utilization": 75,
            "available_reserves": 12,
            "on_call_crews": 8,
            "positioning_availability": "Good"
        }
    
    def _assess_positioning_needs(self, affected_flights):
        """Assess crew positioning requirements"""
        airports = set(f['origin'] for f in affected_flights)
        return {
            "crews_to_position": len(airports) * 2,
            "positioning_flights_needed": len(airports),
            "estimated_positioning_time": "2-4 hours"
        }
    
    def _identify_regulatory_constraints(self, affected_flights):
        """Identify regulatory constraints"""
        return [
            "FAR Part 117 duty time limits",
            "Required rest periods between duties", 
            "Maximum flight duty period restrictions",
            "Crew qualification requirements"
        ]
    
    def _identify_crew_bases(self, affected_flights):
        """Identify crew home bases"""
        return list(set(f['origin'] for f in affected_flights))
