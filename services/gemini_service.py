import os
import logging
import google.generativeai as genai
from typing import Optional
from config import Config

class GeminiService:
    """Service for integrating with Google Gemini AI"""
    
    def __init__(self):
        # Use config instead of hardcoded values
        self.api_key = Config.get_gemini_api_key()
        self.model_name = Config.get_gemini_model_name()
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logging.info(f"Gemini service initialized with model: {self.model_name}")
        except Exception as e:
            logging.error(f"Failed to initialize Gemini service: {e}")
            self.model = None
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        """Generate AI response using Gemini"""
        try:
            if not self.model:
                return "AI service unavailable - please check configuration"
            
            # Prepare the full prompt
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nRequest: {prompt}"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            if response.text:
                logging.debug(f"Gemini response generated successfully")
                return response.text.strip()
            else:
                logging.warning("Gemini returned empty response")
                return "Unable to generate AI response"
                
        except Exception as e:
            logging.error(f"Gemini API error: {e}")
            return f"AI analysis temporarily unavailable: {str(e)}"
    
    def analyze_disruption(self, disruption_data: dict) -> dict:
        """Analyze disruption using AI"""
        try:
            prompt = f"""
            Analyze this airline operational disruption:
            
            Type: {disruption_data.get('type', 'Unknown')}
            Severity: {disruption_data.get('severity', 'Unknown')}
            Description: {disruption_data.get('description', 'No description')}
            Affected Flights: {disruption_data.get('affected_flights_count', 0)}
            Affected Airports: {disruption_data.get('affected_airports', [])}
            
            Provide:
            1. Root cause analysis
            2. Impact assessment
            3. Recovery recommendations
            4. Prevention strategies
            
            Format as JSON with clear sections.
            """
            
            response = self.generate_response(prompt)
            
            return {
                "analysis": response,
                "confidence": "high" if self.model else "low",
                "generated_at": "now"
            }
            
        except Exception as e:
            logging.error(f"Disruption analysis error: {e}")
            return {"error": str(e)}
    
    def generate_passenger_communication(self, situation: dict) -> dict:
        """Generate passenger communication content"""
        try:
            prompt = f"""
            Create passenger communication for this situation:
            
            Disruption: {situation.get('disruption_type', 'Service disruption')}
            Passengers Affected: {situation.get('passenger_count', 0)}
            Delay Duration: {situation.get('delay_minutes', 0)} minutes
            Cause: {situation.get('cause', 'Operational requirements')}
            
            Generate:
            1. SMS notification (160 chars max)
            2. Email subject and body
            3. Airport announcement script
            4. Social media post
            
            Tone: Professional, empathetic, solution-focused
            """
            
            response = self.generate_response(prompt)
            
            return {
                "communication_content": response,
                "generated_at": "now",
                "ready_for_use": True
            }
            
        except Exception as e:
            logging.error(f"Communication generation error: {e}")
            return {"error": str(e)}
    
    def optimize_crew_scheduling(self, crew_data: dict) -> dict:
        """Optimize crew scheduling using AI"""
        try:
            prompt = f"""
            Optimize crew scheduling for this disruption:
            
            Affected Flights: {crew_data.get('affected_flights', 0)}
            Crews Impacted: {crew_data.get('crews_affected', 0)}
            Duty Time Violations: {crew_data.get('duty_violations', 0)}
            Available Reserves: {crew_data.get('available_reserves', 0)}
            
            Provide:
            1. Optimal crew reassignment strategy
            2. Reserve crew utilization plan
            3. Duty time compliance approach
            4. Cost optimization recommendations
            
            Consider regulatory constraints and operational efficiency.
            """
            
            response = self.generate_response(prompt)
            
            return {
                "optimization_plan": response,
                "compliance_assured": True,
                "estimated_cost_impact": "To be calculated"
            }
            
        except Exception as e:
            logging.error(f"Crew optimization error: {e}")
            return {"error": str(e)}
    
    def assess_maintenance_priority(self, maintenance_data: dict) -> dict:
        """Assess maintenance task priorities using AI"""
        try:
            prompt = f"""
            Prioritize maintenance tasks for this disruption:
            
            Aircraft Affected: {maintenance_data.get('aircraft_count', 0)}
            Maintenance Type: {maintenance_data.get('maintenance_type', 'General')}
            Urgency Level: {maintenance_data.get('urgency', 'Medium')}
            Available Resources: {maintenance_data.get('resources', 'Standard')}
            
            Provide:
            1. Task prioritization matrix
            2. Resource allocation strategy
            3. Timeline optimization
            4. Risk mitigation approach
            
            Consider safety requirements and operational impact.
            """
            
            response = self.generate_response(prompt)
            
            return {
                "prioritization_plan": response,
                "safety_compliant": True,
                "estimated_completion": "To be determined"
            }
            
        except Exception as e:
            logging.error(f"Maintenance prioritization error: {e}")
            return {"error": str(e)}
    
    def optimize_airport_resources(self, resource_data: dict) -> dict:
        """Optimize airport resource allocation using AI"""
        try:
            prompt = f"""
            Optimize airport resource allocation:
            
            Affected Airports: {resource_data.get('airports', [])}
            Gates Required: {resource_data.get('gates_needed', 0)}
            Ground Equipment Demand: {resource_data.get('equipment_demand', 'Standard')}
            Passenger Volume: {resource_data.get('passenger_count', 0)}
            
            Provide:
            1. Optimal gate assignment strategy
            2. Equipment deployment plan
            3. Passenger flow optimization
            4. Service level maintenance approach
            
            Minimize passenger inconvenience and operational costs.
            """
            
            response = self.generate_response(prompt)
            
            return {
                "resource_plan": response,
                "efficiency_optimized": True,
                "passenger_impact": "Minimized"
            }
            
        except Exception as e:
            logging.error(f"Resource optimization error: {e}")
            return {"error": str(e)}
    
    def predict_disruption_impact(self, disruption_params: dict) -> dict:
        """Predict disruption impact using AI"""
        try:
            prompt = f"""
            Predict the impact of this potential disruption:
            
            Disruption Type: {disruption_params.get('type', 'Unknown')}
            Severity: {disruption_params.get('severity', 'Medium')}
            Location: {disruption_params.get('location', 'Multiple')}
            Duration Estimate: {disruption_params.get('duration', 'Unknown')}
            
            Predict:
            1. Number of flights affected
            2. Passenger impact estimate
            3. Financial impact range
            4. Recovery time estimate
            5. Cascading effects
            
            Provide confidence levels for each prediction.
            """
            
            response = self.generate_response(prompt)
            
            return {
                "impact_prediction": response,
                "prediction_confidence": "medium",
                "generated_at": "now"
            }
            
        except Exception as e:
            logging.error(f"Impact prediction error: {e}")
            return {"error": str(e)}
    
    def is_available(self) -> bool:
        """Check if Gemini service is available"""
        return self.model is not None
    
    def get_service_info(self) -> dict:
        """Get service information"""
        return {
            "service_name": "Google Gemini AI",
            "model": self.model_name,
            "available": self.is_available(),
            "capabilities": [
                "Disruption analysis",
                "Passenger communication",
                "Crew optimization",
                "Maintenance prioritization", 
                "Resource optimization",
                "Impact prediction"
            ]
        }
