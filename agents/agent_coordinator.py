from datetime import datetime
from typing import Dict, List, Any
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from models import Disruption, AgentCommunication
from .passenger_rebooking_agent import PassengerRebookingAgent
from .crew_scheduling_agent import CrewSchedulingAgent
from .aircraft_maintenance_agent import AircraftMaintenanceAgent
from .airport_resource_agent import AirportResourceAgent
from .customer_communication_agent import CustomerCommunicationAgent
import json
from mongo_utils import mongo_db

try:
    from config import Config
    from agents_adk.loop_agent import LoopAgent
    from agents_adk.parallel_agent import ParallelAgent
    from agents_adk.sequential_agent import SequentialAgent
    from agents_adk.minimal_llm_agent import MinimalLLMAgent
    from agents_adk.session_persistence_agent import SessionPersistenceAgent
    from agents_adk.interactive_cli_agent import InteractiveCLIAgent
    from agents_adk.event_handling_robust_agent import EventHandlingRobustAgent
    from agents_adk.external_api_tool_agent import ExternalAPIToolAgent
    from agents_adk.workflow_agents import WorkflowAgent
    from agents_adk.nested_agent_tool_agent import NestedAgentToolAgent
    from agents_adk.multi_tool_agent import MultiToolAgent
    from agents_adk.configurable_prompt_agent import ConfigurablePromptAgent
    from agents_adk.single_tool_agent import SingleToolAgent
    from agents_adk.domain_agent_1 import DomainAgent1
    from agents_adk.domain_agent_2 import DomainAgent2
    from agents_adk.domain_agent_3 import DomainAgent3
    from agents_adk.coordinator_agent import CoordinatorAgent
except ImportError:
    # ADK agents not available or not needed
    pass

class AgentCoordinator:
    """Coordinates multi-agent responses to IROPS disruptions"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.app = None  # No longer create a Flask app instance here
        logging.info("Agent Coordinator initialized, agents not yet created.")
        self.adk_agents = None
        if hasattr(Config, 'USE_ADK_AGENTS') and Config.USE_ADK_AGENTS:
            self.adk_agents = {
                'loop': LoopAgent(name='LoopAgent'),
                'parallel': ParallelAgent(name='ParallelAgent'),
                'sequential': SequentialAgent(name='SequentialAgent'),
                # ... add other ADK agents as needed, with required fields ...
            }
            # Clean, emoji-rich summary log for ADK agent status
            adk_names = ', '.join(self.adk_agents.keys())
            print(f"🧑‍💻🤖 ADK Agents integrated: {adk_names} ✅")
            # Minimal demonstration: run a simple method on one ADK agent (no log)
            try:
                _ = self.adk_agents['loop'].run() if hasattr(self.adk_agents['loop'], 'run') else None
            except Exception:
                pass
    
    def init_agents(self, app=None):
        """Create agent instances within the app context"""
        if self.agents:
            logging.info("Agents already initialized.")
            return
        self.agents = {
            'passenger_rebooking': PassengerRebookingAgent(),
            'crew_scheduling': CrewSchedulingAgent(),
            'aircraft_maintenance': AircraftMaintenanceAgent(),
            'airport_resource': AirportResourceAgent(),
            'customer_communication': CustomerCommunicationAgent()
        }
        logging.info("Specialized agents created and initialized.")
    
    def coordinate_disruption_response(self, disruption_id: int) -> dict:
        """Main coordination method for disruption response (MongoDB)"""
        if not self.agents:
            logging.error("Agents not initialized. Call init_agents() first.")
            return {"success": False, "error": "Agents not initialized"}
        try:
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return {"success": False, "error": "Disruption not found"}
            logging.info(f"Starting coordination for disruption {disruption_id}: {disruption.get('type')}")
            # Phase 1: Immediate Assessment (Parallel)
            assessment_results = self._execute_parallel_assessment(disruption_id)
            # Phase 2: Coordination and Planning (Sequential)
            coordination_plan = self._create_coordination_plan(assessment_results)
            # Phase 3: Execution (Coordinated)
            execution_results = self._execute_coordinated_response(coordination_plan, disruption_id)
            # Phase 4: Monitoring and Communication
            self._initiate_monitoring_phase(disruption_id, execution_results)
            # Compile final response
            response = {
                "success": True,
                "disruption_id": disruption_id,
                "coordination_phases": ["Assessment", "Planning", "Execution", "Monitoring"],
                "agents_involved": len(self.agents),
                "assessment_results": assessment_results,
                "coordination_plan": coordination_plan,
                "execution_results": execution_results,
                "next_review": (datetime.utcnow().timestamp() + 1800)
            }
            self._log_coordination_activity(disruption_id, response)
            # Test: Create a direct communication record to verify MongoDB is working
            try:
                test_comm = {
                    'sender': "Agent Coordinator",
                    'receiver': "System",
                    'message_type': "coordination_complete",
                    'content': json.dumps({"disruption_id": disruption_id, "status": "completed"}),
                    'processed': False,
                    'disruption_id': disruption_id,
                    'timestamp': datetime.utcnow().isoformat()
                }
                mongo_db['agent_communications'].insert_one(test_comm)
                logging.info(f"Test communication record created for disruption {disruption_id}")
            except Exception as e:
                logging.error(f"Failed to create test communication record: {e}")
            return response
        except Exception as e:
            logging.error(f"Coordination error for disruption {disruption_id}: {e}")
            return {"success": False, "error": str(e)}
    
    def _execute_parallel_assessment(self, disruption_id: int) -> Dict[str, Any]:
        """Execute parallel assessment by all agents"""
        assessment_tasks = {}
        for agent_name, agent in self.agents.items():
            def task_with_context(agent=agent):
                try:
                    return agent.analyze_situation({"disruption_id": disruption_id})
                except Exception as e:
                    logging.error(f"Assessment error in {agent.name}: {e}")
                    return {"error": str(e)}
            task = self.executor.submit(task_with_context)
            assessment_tasks[agent_name] = task
        assessment_results = {}
        for agent_name, task in assessment_tasks.items():
            try:
                logging.debug(f"Waiting for assessment result from {agent_name}")
                result = task.result(timeout=3)
                assessment_results[agent_name] = result
                logging.debug(f"Assessment completed by {agent_name}")
            except Exception as e:
                logging.error(f"Assessment failed for {agent_name}: {e}")
                assessment_results[agent_name] = {"error": str(e)}
        return assessment_results
    
    def _create_coordination_plan(self, assessment_results: Dict[str, Any]) -> Dict[str, Any]:
        """Create coordinated response plan based on assessments"""
        plan = {
            "priority_sequence": [],
            "dependencies": {},
            "resource_allocations": {},
            "communication_flow": [],
            "success_metrics": {}
        }
        
        # Determine priority sequence based on disruption impact
        priority_agents = self._determine_agent_priority(assessment_results)
        plan["priority_sequence"] = priority_agents
        
        # Map dependencies between agents
        plan["dependencies"] = {
            "passenger_rebooking": ["crew_scheduling", "aircraft_maintenance"],
            "customer_communication": ["passenger_rebooking", "airport_resource"],
            "airport_resource": ["aircraft_maintenance"],
            "crew_scheduling": [],
            "aircraft_maintenance": []
        }
        
        # Define communication flow
        plan["communication_flow"] = [
            {"from": "Aircraft Maintenance Agent", "to": "Crew Scheduling Agent", "message": "maintenance_status"},
            {"from": "Crew Scheduling Agent", "to": "Passenger Rebooking Agent", "message": "crew_availability"},
            {"from": "Passenger Rebooking Agent", "to": "Customer Communication Agent", "message": "rebooking_status"},
            {"from": "Airport Resource Agent", "to": "Customer Communication Agent", "message": "facility_status"}
        ]
        
        return plan
    
    def _execute_coordinated_response(self, coordination_plan: Dict[str, Any], disruption_id: int) -> Dict[str, Any]:
        """Execute coordinated response following the plan"""
        execution_results = {}
        completed_agents = set()
        logging.info(f"Starting coordinated response execution for disruption {disruption_id}")
        logging.info(f"Priority sequence: {coordination_plan['priority_sequence']}")
        for agent_name in coordination_plan["priority_sequence"]:
            logging.info(f"Executing agent: {agent_name}")
            dependencies = coordination_plan["dependencies"].get(agent_name, [])
            if not all(dep in completed_agents for dep in dependencies):
                logging.warning(f"Dependencies not met for {agent_name}, but executing anyway due to coordination plan")
            try:
                agent = self.agents[agent_name]
                result = agent.process_disruption(disruption_id)
                execution_results[agent_name] = result
                completed_agents.add(agent_name)
                logging.info(f"Agent {agent_name} completed successfully")
                self._process_agent_communications(agent_name, coordination_plan, result, disruption_id)
                logging.info(f"Agent {agent_name} completed disruption processing")
            except Exception as e:
                logging.error(f"Execution failed for {agent_name}: {e}")
                execution_results[agent_name] = {"success": False, "error": str(e)}
        logging.info(f"Coordinated response execution completed for disruption {disruption_id}")
        return execution_results
    
    def _initiate_monitoring_phase(self, disruption_id: int, execution_results: Dict[str, Any]):
        """Initiate ongoing monitoring of the disruption response"""
        monitoring_config = {
            "disruption_id": disruption_id,
            "monitoring_interval": 300,  # 5 minutes
            "agents_to_monitor": list(self.agents.keys()),
            "success_criteria": {
                "passenger_rebooking": "rebooking_completion_rate > 90%",
                "crew_scheduling": "duty_compliance = 100%",
                "aircraft_maintenance": "aircraft_availability_restored",
                "airport_resource": "normal_operations_resumed",
                "customer_communication": "passenger_satisfaction > 80%"
            }
        }
        
        # Log monitoring initiation
        logging.info(f"Monitoring initiated for disruption {disruption_id}")
        
        # In a real system, this would set up background monitoring tasks
        return monitoring_config
    
    def _determine_agent_priority(self, assessment_results: Dict[str, Any]) -> List[str]:
        """Determine agent execution priority based on assessments"""
        # Default priority order - ensure all agents are included
        default_priority = [
            "aircraft_maintenance",  # Must resolve technical issues first
            "crew_scheduling",       # Then ensure crew availability
            "airport_resource",      # Secure airport resources
            "passenger_rebooking",   # Then handle passenger rebooking
            "customer_communication" # Finally communicate with passengers
        ]
        
        # Adjust based on disruption characteristics
        priority_adjustments = {}
        
        # Check for critical maintenance needs
        maintenance_result = assessment_results.get("aircraft_maintenance", {})
        if maintenance_result.get("maintenance_urgency") == "critical":
            priority_adjustments["aircraft_maintenance"] = 1
        
        # Check for crew duty violations
        crew_result = assessment_results.get("crew_scheduling", {})
        if crew_result.get("duty_time_risk", {}).get("high_risk_crews", 0) > 0:
            priority_adjustments["crew_scheduling"] = 2
        
        # Check for high passenger impact
        passenger_result = assessment_results.get("passenger_rebooking", {})
        if passenger_result.get("passenger_impact", {}).get("total_affected", 0) > 500:
            priority_adjustments["customer_communication"] = 1
        
        # Apply adjustments (lower number = higher priority)
        adjusted_priority = sorted(default_priority, 
                                 key=lambda x: priority_adjustments.get(x, 5))
        
        # Ensure all agents are included
        all_agents = set(self.agents.keys())
        missing_agents = all_agents - set(adjusted_priority)
        if missing_agents:
            adjusted_priority.extend(list(missing_agents))
        
        return adjusted_priority
    
    def _process_agent_communications(self, agent_name: str, coordination_plan: dict, result: dict, disruption_id: int):
        """Process inter-agent communications based on coordination plan (MongoDB)"""
        communication_flows = coordination_plan.get("communication_flow", [])
        for flow in communication_flows:
            if flow["from"] == agent_name:
                try:
                    comm_doc = {
                        'sender': self.agents[agent_name].name,
                        'receiver': flow["to"],
                        'message_type': flow["message"],
                        'content': json.dumps(result),
                        'processed': False,
                        'disruption_id': disruption_id,
                        'timestamp': datetime.utcnow().isoformat()
                    }
                    mongo_db['agent_communications'].insert_one(comm_doc)
                    logging.info(f"Communication sent: {agent_name} -> {flow['to']}")
                except Exception as e:
                    logging.error(f"Failed to create communication record: {e}")
    
    def _log_coordination_activity(self, disruption_id: int, response: Dict[str, Any]):
        """Log coordination activity for audit and analysis"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "disruption_id": disruption_id,
            "coordination_success": response.get("success", False),
            "agents_involved": response.get("agents_involved", 0),
            "phases_completed": len(response.get("coordination_phases", [])),
            "errors": [result.get("error") for result in response.get("execution_results", {}).values() if result.get("error")]
        }
        
        logging.info(f"Coordination completed for disruption {disruption_id}: {log_entry}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get current status of all agents"""
        status = {}
        for agent_name, agent in self.agents.items():
            try:
                status[agent_name] = agent.get_agent_info()
            except Exception as e:
                logging.error(f"Failed to get status for {agent_name}: {e}")
                status[agent_name] = {"error": str(e)}
        return status
    
    def process_agent_messages(self, agent_name: str) -> List[Dict[str, Any]]:
        """Process pending messages for a specific agent"""
        if agent_name not in self.agents:
            return []
        agent = self.agents[agent_name]
        try:
            messages = agent.get_unprocessed_messages()
            processed_messages = []
            for message in messages:
                try:
                    response = self._handle_agent_message(agent, message)
                    agent.mark_message_processed(message.id)
                    processed_messages.append({
                        "message_id": message.id,
                        "sender": message.sender,
                        "message_type": message.message_type,
                        "processed_at": datetime.utcnow().isoformat(),
                        "response": response
                    })
                except Exception as e:
                    logging.error(f"Failed to process message {message.id}: {e}")
            return processed_messages
        except Exception as e:
            logging.error(f"Failed to process messages for {agent_name}: {e}")
            return []
    
    def _handle_agent_message(self, agent, message) -> Dict[str, Any]:
        """Handle a specific agent message"""
        message_type = message.message_type
        content = message.content_dict
        
        if message_type == "status_request":
            return agent.get_agent_info()
        elif message_type == "task_assignment":
            return agent.execute_task(content.get("task_type"), content.get("parameters", {}))
        elif message_type in ["maintenance_status", "crew_availability", "rebooking_status", "facility_status"]:
            # Handle coordination messages
            return {"acknowledged": True, "timestamp": datetime.utcnow().isoformat()}
        else:
            return {"error": f"Unknown message type: {message_type}"}
    
    def shutdown(self):
        """Shutdown the coordinator and clean up resources"""
        self.executor.shutdown(wait=True)
        logging.info("Agent Coordinator shutdown completed")
