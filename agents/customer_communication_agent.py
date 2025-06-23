from .base_agent import BaseAgent
from mongo_utils import mongo_db
from services.gemini_service import GeminiService
from datetime import datetime, timedelta
import logging

class CustomerCommunicationAgent(BaseAgent):
    """Agent specialized in customer communication and passenger experience"""
    
    def __init__(self):
        super().__init__("Customer Communication Agent", "customer_communication")
        self.capabilities = [
            "passenger_notifications",
            "multi_channel_communication",
            "sentiment_analysis",
            "proactive_messaging",
            "compensation_coordination"
        ]
        self.gemini_service = GeminiService()
    
    def process_disruption(self, disruption_id: int) -> dict:
        """Process disruption for customer communication (MongoDB)"""
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            affected_flight_ids = disruption.get('affected_flight_list', [])
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': affected_flight_ids}}))
            
            # Get context from other agents
            rebooking_messages = self._get_disruption_messages(disruption_id, sender_name="passenger_rebooking")
            rebooking_context = rebooking_messages[0] if rebooking_messages else {}
            
            airport_messages = self._get_disruption_messages(disruption_id, sender_name="airport_resource")
            airport_context = airport_messages[0] if airport_messages else {}

            # Calculate passenger impact
            passenger_impact = self._calculate_passenger_impact(affected_flights)
            
            # Generate AI-powered communication drafts
            ai_drafts = self._get_ai_communication_drafts(disruption, passenger_impact["total_passengers"], rebooking_context, airport_context)
            
            # Create communication plan
            communication_plan = self._create_communication_plan(ai_drafts)
            
            # Generate AI-powered communication content
            ai_content = self._generate_ai_communication_content(disruption, passenger_impact)
            
            # Assess compensation requirements
            compensation_assessment = self._assess_compensation_requirements(disruption, affected_flights)
            
            result = {
                "success": True,
                "agent": self.name,
                "disruption_id": disruption_id,
                "passengers_to_notify": passenger_impact["total_passengers"],
                "communication_channels": len(communication_plan["channels"]),
                "communications_sent": 0,  # Placeholder
                "communication_plan": communication_plan,
                "ai_drafts": ai_drafts,
                "rebooking_context": rebooking_context,
                "airport_context": airport_context,
                "ai_content": ai_content,
                "compensation_assessment": compensation_assessment,
                "estimated_response_time": "15 minutes"
            }
            
            # Log communication activity
            self._log_communication_activity(disruption_id, passenger_impact["total_passengers"])
            
            return result
            
        except Exception as e:
            logging.error(f"Customer communication processing error: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_situation(self, context: dict) -> dict:
        """Analyze customer communication situation (MongoDB)"""
        try:
            disruption_id = context.get('disruption_id')
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"error": "Disruption not found"}
            affected_flights = list(mongo_db['flights'].find({'id': {'$in': disruption.get('affected_flight_list', [])}}))
            
            analysis = {
                "communication_urgency": self._assess_communication_urgency(disruption, affected_flights),
                "passenger_sentiment_risk": self._assess_sentiment_risk(disruption, affected_flights),
                "channel_requirements": self._determine_channel_requirements(affected_flights),
                "message_complexity": self._assess_message_complexity(disruption),
                "compensation_exposure": self._estimate_compensation_exposure(disruption, affected_flights)
            }
            
            return analysis
            
        except Exception as e:
            logging.error(f"Customer communication situation analysis error: {e}")
            return {"error": str(e)}
    
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate customer communication recommendations"""
        recommendations = []
        
        try:
            urgency = analysis.get("communication_urgency", "medium")
            if urgency == "critical":
                recommendations.append({
                    "priority": "critical",
                    "action": "Send immediate proactive notifications to all affected passengers",
                    "rationale": "High-impact disruption requires immediate passenger awareness"
                })
            
            sentiment_risk = analysis.get("passenger_sentiment_risk", "medium")
            if sentiment_risk == "high":
                recommendations.append({
                    "priority": "high",
                    "action": "Deploy empathetic messaging with clear action steps",
                    "rationale": "High sentiment risk requires careful communication approach"
                })
            
            channels = analysis.get("channel_requirements", {})
            if channels.get("multi_channel_required", False):
                recommendations.append({
                    "priority": "medium",
                    "action": "Activate all communication channels (SMS, email, app, social)",
                    "rationale": "Broad passenger base requires multi-channel approach"
                })
            
            compensation = analysis.get("compensation_exposure", {})
            if compensation.get("risk_level") == "high":
                recommendations.append({
                    "priority": "medium",
                    "action": "Prepare compensation processing and clear policy communication",
                    "rationale": "Significant compensation exposure requires proactive management"
                })
            
        except Exception as e:
            logging.error(f"Communication recommendation generation error: {e}")
        
        return recommendations
    
    def _calculate_passenger_impact(self, affected_flights):
        """Calculate total passenger impact"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        
        # Categorize passengers
        passenger_categories = {
            "business_travelers": int(total_passengers * 0.4),
            "leisure_travelers": int(total_passengers * 0.5), 
            "connecting_passengers": int(total_passengers * 0.3),
            "international_passengers": int(total_passengers * 0.2)
        }
        
        return {
            "total_passengers": total_passengers,
            "passenger_categories": passenger_categories,
            "high_value_customers": int(total_passengers * 0.15),  # Estimate elite members
            "special_assistance_required": int(total_passengers * 0.05)  # Estimate special needs
        }
    
    def _create_communication_plan(self, ai_drafts):
        """Create comprehensive communication plan"""
        plan = {
            "approach": "proactive_multi_channel",
            "channels": [
                {"channel": "SMS", "priority": 1, "reach": "100%"},
                {"channel": "Email", "priority": 2, "reach": "90%"},
                {"channel": "Mobile App", "priority": 3, "reach": "60%"},
                {"channel": "Airport Announcements", "priority": 4, "reach": "30%"}
            ],
            "messaging_timeline": {
                "immediate": "Initial disruption notification",
                "15_minutes": "Detailed situation update with options",
                "30_minutes": "Rebooking and compensation information",
                "hourly": "Progress updates until resolution"
            },
            "tone": "empathetic_professional",
            "key_messages": [
                "We apologize for the inconvenience",
                "We are working to resolve this situation",
                "Alternative options are being arranged",
                "Compensation will be provided as appropriate"
            ],
            "ai_drafts": ai_drafts
        }
        
        return plan
    
    def _create_passenger_notifications(self, disruption, affected_flights):
        """Create specific passenger notifications"""
        notifications = []
        
        for flight in affected_flights[:5]:  # Limit for demo
            notification = {
                "flight_number": flight.get('flight_number', ''),
                "notification_type": "disruption_alert",
                "channels": ["SMS", "Email", "App"],
                "message": f"Important update for {flight.get('flight_number', '')}: {disruption.get('description', '')}",
                "action_required": "Please check rebooking options",
                "urgency": "high" if disruption.get('severity', '') in ["high", "critical"] else "medium",
                "estimated_passengers": flight.get('passenger_count', 0)
            }
            notifications.append(notification)
        
        # Add general disruption notification
        if len(affected_flights) > 1:
            notifications.append({
                "flight_number": "Multiple flights",
                "notification_type": "general_disruption",
                "channels": ["Email", "App", "Website"],
                "message": f"Service disruption affecting multiple flights: {disruption.get('description', '')}",
                "action_required": "Check flight status and rebooking options",
                "urgency": disruption.get('severity', ''),
                "estimated_passengers": sum(f.get('passenger_count', 0) for f in affected_flights)
            })
        
        return notifications
    
    def _generate_ai_communication_content(self, disruption, passenger_impact):
        """Generate AI-powered communication content"""
        try:
            context = f"""
            Disruption: {disruption.get('type', '')} - {disruption.get('severity', '')}
            Description: {disruption.get('description', '')}
            Passengers Affected: {passenger_impact['total_passengers']}
            Business Travelers: {passenger_impact['passenger_categories']['business_travelers']}
            Connecting Passengers: {passenger_impact['passenger_categories']['connecting_passengers']}
            """
            
            prompt = f"""
            As an airline customer service specialist, create passenger communication content for this disruption:
            
            {context}
            
            Generate:
            1. Empathetic initial notification message (SMS/Email)
            2. Detailed explanation with next steps (Email/App)
            3. Social media statement (if needed)
            4. Airport announcement script
            5. FAQ responses for common passenger questions
            
            Tone should be professional, empathetic, and solution-focused.
            Include clear actions passengers can take.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_content": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI communication content error: {e}")
            return {"error": "AI content generation unavailable"}
    
    def _assess_compensation_requirements(self, disruption, affected_flights):
        """Assess compensation requirements and eligibility"""
        assessment = {
            "compensation_eligible": False,
            "compensation_type": "none",
            "estimated_cost": 0,
            "eligibility_criteria": []
        }
        
        # Determine compensation eligibility based on delay duration and cause
        significant_delays = [f for f in affected_flights if f.get('delay_minutes', 0) and f.get('delay_minutes', 0) > 180]
        
        if significant_delays and disruption.get('type', '') in ["mechanical", "crew"]:
            assessment["compensation_eligible"] = True
            assessment["compensation_type"] = "monetary_voucher" 
            assessment["estimated_cost"] = len(significant_delays) * 250  # Average per passenger
            assessment["eligibility_criteria"] = [
                "Delay exceeds 3 hours",
                "Cause within airline control",
                "Domestic/international flight regulations apply"
            ]
        elif significant_delays:
            assessment["compensation_eligible"] = True
            assessment["compensation_type"] = "service_recovery"
            assessment["estimated_cost"] = len(significant_delays) * 50  # Vouchers/amenities
            assessment["eligibility_criteria"] = [
                "Meal vouchers for extended delays",
                "Hotel accommodation if overnight",
                "Transportation allowances"
            ]
        
        return assessment
    
    def _determine_communication_approach(self, disruption):
        """Determine overall communication approach"""
        if disruption.get('severity', '') == "critical":
            return "Crisis communication - immediate, frequent, transparent"
        elif disruption.get('severity', '') == "high":
            return "Proactive communication - regular updates, clear actions"
        else:
            return "Standard communication - timely updates, solution-focused"
    
    def _determine_communication_tone(self, disruption):
        """Determine appropriate communication tone"""
        if disruption.get('type', '') == "weather":
            return "Understanding and supportive - acknowledge circumstances beyond control"
        elif disruption.get('type', '') in ["mechanical", "crew"]:
            return "Apologetic and solution-focused - take responsibility, focus on resolution"
        else:
            return "Professional and informative - clear facts and options"
    
    def _create_key_messages(self, disruption, affected_flights):
        """Create key messaging points"""
        return [
            f"We are addressing a {disruption.get('type', '')} disruption affecting {len(affected_flights)} flights",
            "Passenger safety is our top priority",
            "We are working to minimize inconvenience and restore normal operations",
            "Multiple rebooking options are available",
            "Customer service teams are standing by to assist",
            "Regular updates will be provided as the situation develops"
        ]
    
    def _assess_communication_urgency(self, disruption, affected_flights):
        """Assess urgency of communication"""
        if disruption.get('severity', '') == "critical":
            return "critical"
        elif len(affected_flights) > 10 or sum(f.get('passenger_count', 0) for f in affected_flights) > 1000:
            return "high"
        else:
            return "medium"
    
    def _assess_sentiment_risk(self, disruption, affected_flights):
        """Assess risk of negative passenger sentiment"""
        risk_factors = 0
        
        # Check for high-impact factors
        if disruption.get('type', '') in ["mechanical", "crew"]:  # Airline controllable
            risk_factors += 2
        
        if disruption.get('severity', '') in ["high", "critical"]:
            risk_factors += 2
        
        if any(f.get('delay_minutes', 0) and f.get('delay_minutes', 0) > 240 for f in affected_flights):  # 4+ hour delays
            risk_factors += 2
        
        if len(affected_flights) > 15:  # Large scale disruption
            risk_factors += 1
        
        if risk_factors >= 4:
            return "high"
        elif risk_factors >= 2:
            return "medium"
        else:
            return "low"
    
    def _determine_channel_requirements(self, affected_flights):
        """Determine communication channel requirements"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        
        return {
            "multi_channel_required": total_passengers > 200,
            "social_media_needed": total_passengers > 500,
            "priority_channels": ["SMS", "Email", "App"],
            "secondary_channels": ["Social Media", "Website"] if total_passengers > 500 else ["Website"]
        }
    
    def _assess_message_complexity(self, disruption):
        """Assess complexity of messaging required"""
        if disruption.get('type', '') == "weather":
            return "low"  # Simple weather explanation
        elif disruption.get('type', '') in ["mechanical", "crew"]:
            return "high"  # Need to explain technical/operational issues
        else:
            return "medium"
    
    def _estimate_compensation_exposure(self, disruption, affected_flights):
        """Estimate financial exposure from compensation"""
        total_passengers = sum(f.get('passenger_count', 0) for f in affected_flights)
        significant_delays = sum(1 for f in affected_flights if f.get('delay_minutes', 0) and f.get('delay_minutes', 0) > 180)
        
        if significant_delays > 5 and disruption.get('type', '') in ["mechanical", "crew"]:
            return {
                "risk_level": "high",
                "estimated_cost": total_passengers * 200,
                "affected_passengers": total_passengers
            }
        elif significant_delays > 0:
            return {
                "risk_level": "medium", 
                "estimated_cost": total_passengers * 75,
                "affected_passengers": total_passengers
            }
        else:
            return {
                "risk_level": "low",
                "estimated_cost": 0,
                "affected_passengers": 0
            }
    
    def _log_communication_activity(self, disruption_id, passenger_count):
        """Log communication activity for tracking"""
        logging.info(f"Communication initiated for disruption {disruption_id} affecting {passenger_count} passengers")

    def _get_ai_communication_drafts(self, disruption, total_passengers, rebooking_context, airport_context):
        """Get AI-powered communication drafts"""
        try:
            context = f"""
            Disruption: {disruption.get('type', '')} - {disruption.get('severity', '')}
            Description: {disruption.get('description', '')}
            Total Passengers Affected: {total_passengers}
            Rebooking Status: {rebooking_context.get('status', 'Pending')}
            Airport Facility Status: {airport_context.get('status', 'Operational')}
            """
            
            prompt = f"""
            As an airline customer communications specialist, analyze this disruption situation:
            
            {context}
            
            Generate:
            1. AI-powered communication drafts for different channels
            2. Relevant context from other agents
            3. Recommendations for communication strategy
            
            Tone should be professional, empathetic, and solution-focused.
            Include clear actions passengers can take.
            """
            
            response = self.gemini_service.generate_response(prompt)
            return {"ai_drafts": response, "generated_at": datetime.utcnow().isoformat()}
            
        except Exception as e:
            logging.error(f"AI communication drafts error: {e}")
            return {"error": "AI drafts generation unavailable"}
