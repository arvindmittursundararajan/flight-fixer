from abc import ABC, abstractmethod
from datetime import datetime
from mongo_utils import mongo_db
import json
import logging
from models import AgentStatus

class BaseAgent(ABC):
    """Abstract base class for all IROPS agents"""
    
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.capabilities = []
        
        # Ensure agent exists in database
        self._ensure_agent_exists()
    
    def _ensure_agent_exists(self):
        """Ensure agent record exists in MongoDB"""
        try:
            from flask import has_app_context
            if not has_app_context():
                logging.info(f"Skipping agent DB record creation for {self.name} - no app context")
                return
            agent = mongo_db['agents'].find_one({'name': self.name})
            if not agent:
                agent_doc = {
                    'name': self.name,
                    'type': self.agent_type,
                    'status': self.status,
                    'capabilities': self.capabilities,
                    'current_task': self.current_task,
                    'last_activity': datetime.utcnow().isoformat()
                }
                mongo_db['agents'].insert_one(agent_doc)
                logging.info(f"Created agent record: {self.name}")
        except Exception as e:
            logging.error(f"Error creating agent record: {e}")
    
    def update_status(self, status, task: str = None):
        """Update agent status in MongoDB"""
        try:
            update = {'status': status, 'last_activity': datetime.utcnow().isoformat()}
            if task is not None:
                update['current_task'] = task
            mongo_db['agents'].update_one({'name': self.name}, {'$set': update})
            self.status = status
            self.current_task = task
            logging.debug(f"Agent {self.name} status updated: {status}")
        except Exception as e:
            logging.error(f"Error updating agent status: {e}")
    
    def send_message(self, receiver: str, message_type: str, content: dict):
        """Send message to another agent (MongoDB)"""
        try:
            comm_doc = {
                'sender': self.name,
                'receiver': receiver,
                'message_type': message_type,
                'content': json.dumps(content),
                'processed': False,
                'timestamp': datetime.utcnow().isoformat()
            }
            mongo_db['agent_communications'].insert_one(comm_doc)
            logging.info(f"Message sent: {self.name} -> {receiver} ({message_type})")
            return True
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False
    
    def get_unprocessed_messages(self):
        """Get unprocessed messages for this agent (MongoDB)"""
        try:
            messages = list(mongo_db['agent_communications'].find({
                'receiver': self.name,
                'processed': False
            }).sort('timestamp', 1))
            return messages
        except Exception as e:
            logging.error(f"Error getting messages: {e}")
            return []
    
    def mark_message_processed(self, message_id):
        """Mark a message as processed (MongoDB)"""
        try:
            mongo_db['agent_communications'].update_one({'_id': message_id}, {'$set': {'processed': True}})
            logging.debug(f"Message {message_id} marked as processed")
        except Exception as e:
            logging.error(f"Error marking message processed: {e}")
    
    def _get_disruption_messages(self, disruption_id: int, sender_name: str = None) -> list:
        """Retrieve and parse messages for a given disruption (MongoDB)"""
        messages_content = []
        try:
            query = {
                'receiver': self.name,
                'disruption_id': disruption_id
            }
            if sender_name:
                query['sender'] = sender_name
            messages = list(mongo_db['agent_communications'].find(query).sort('timestamp', 1))
            for msg in messages:
                try:
                    content_dict = json.loads(msg.get('content', '{}'))
                except:
                    content_dict = {}
                messages_content.append(content_dict)
                # Mark message as processed once it's been read
                self.mark_message_processed(msg.get('_id'))
        except Exception as e:
            logging.error(f"Error retrieving messages for disruption {disruption_id}: {e}")
        return messages_content
    
    @abstractmethod
    def process_disruption(self, disruption_id: int) -> dict:
        """Process a disruption - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def analyze_situation(self, context: dict) -> dict:
        """Analyze the current situation - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def generate_recommendations(self, analysis: dict) -> list:
        """Generate recommendations based on analysis"""
        pass
    
    def execute_task(self, task_type: str, parameters: dict) -> dict:
        """Execute a specific task"""
        self.update_status(AgentStatus.PROCESSING, f"Executing {task_type}")
        
        try:
            if task_type == "process_disruption":
                result = self.process_disruption(parameters.get('disruption_id'))
            elif task_type == "analyze_situation":
                result = self.analyze_situation(parameters)
            elif task_type == "generate_recommendations":
                result = self.generate_recommendations(parameters)
            else:
                result = {"success": False, "error": f"Unknown task type: {task_type}"}
            
            self.update_status(AgentStatus.ACTIVE, "Ready for next task")
            return result
            
        except Exception as e:
            logging.error(f"Task execution error in {self.name}: {e}")
            self.update_status(AgentStatus.ERROR, f"Error: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_agent_info(self) -> dict:
        """Get current agent information"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "status": self.status.value,
            "current_task": self.current_task,
            "capabilities": self.capabilities
        }
