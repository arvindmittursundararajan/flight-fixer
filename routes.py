from flask import render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, timedelta
from models import Flight, Disruption, Agent, AgentCommunication, Scenario, DisruptionType, AgentStatus, AgentType
from agents.agent_coordinator import AgentCoordinator
from services.data_simulator import DataSimulator
from services.business_metrics_service import BusinessMetricsService
from coordination_test_utils import CoordinationTestRunner, TestResult, quick_coordination_test, quick_communications_test, quick_system_check
import json
import logging
from mongo_utils import mongo_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global coordinator instance
coordinator = None
business_metrics_service = BusinessMetricsService()

def init_app(app):
    """Initialize the application with routes"""
    global coordinator
    
    # Initialize agent coordinator
    coordinator = AgentCoordinator()
    coordinator.init_agents(app)
    
    # Register routes
    register_routes(app)

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def dashboard():
        """Dashboard page (MongoDB version)"""
        try:
            today = datetime.utcnow().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            # Total flights today
            total_flights_today = mongo_db['flights'].count_documents({
                'scheduled_departure': {'$gte': today_start.isoformat(), '$lte': today_end.isoformat()}
            })

            # Delayed flights
            delayed_flights = list(mongo_db['flights'].find({
                'delay_minutes': {'$gt': 0},
                'scheduled_departure': {'$gte': today_start.isoformat(), '$lte': today_end.isoformat()}
            }))

            # Active disruptions
            active_disruptions = list(mongo_db['disruptions'].find({'status': 'active'}))
            
            on_time_flights = total_flights_today - len(delayed_flights)
            on_time_percentage = round((on_time_flights / total_flights_today) * 100) if total_flights_today > 0 else 100
            
            metrics = {
                'total_flights_today': total_flights_today,
                'delayed_flights': len(delayed_flights),
                'active_disruptions': len(active_disruptions),
                'on_time_percentage': on_time_percentage
            }
            
            # Upcoming flights (next 12 hours)
            upcoming_flights = list(mongo_db['flights'].find({
                'scheduled_departure': {'$gte': datetime.utcnow().isoformat(), '$lte': (datetime.utcnow() + timedelta(hours=12)).isoformat()}
            }).sort('scheduled_departure', 1).limit(10))
            
            # Agents
            agents = list(mongo_db['agents'].find())
            agent_status = {}
            for agent in agents:
                agent_status[agent['name']] = {
                    'name': agent['name'],
                    'status': agent.get('status', 'unknown'),
                    'current_task': agent.get('current_task'),
                    'last_activity': agent.get('last_activity')
                }
            
            # Recent communications
            recent_communications = list(mongo_db['agent_communications'].find().sort('timestamp', -1).limit(10))
            
            return render_template('dashboard.html',
                                metrics=metrics,
                                active_disruptions=active_disruptions,
                                delayed_flights=delayed_flights,
                                resolved_today=12,  # Default value for resolved today
                                upcoming_flights=upcoming_flights,
                                agent_status=agent_status,
                                recent_communications=recent_communications)
        except Exception as e:
            logger.error(f"Error in dashboard route (MongoDB): {e}")
            return render_template('dashboard.html', error=str(e))

    @app.route('/agents')
    def agents():
        """Agents page (MongoDB version)"""
        try:
            # Get all agents
            agents_list = list(mongo_db['agents'].find())
            
            # Generate agent metrics
            agent_metrics = {}
            demo_success_rates = [94, 98, 91, 89, 96]
            for idx, agent in enumerate(agents_list):
                sent_comms = mongo_db['agent_communications'].count_documents({'sender': agent['name']})
                received_comms = mongo_db['agent_communications'].count_documents({'receiver': agent['name']})
                agent_metrics[agent['name']] = {
                    'tasks_completed': sent_comms + received_comms,
                    'success_rate': demo_success_rates[idx % len(demo_success_rates)],
                    'average_response_time': 2.3,
                    'current_workload': 'Low' if agent.get('status') == 'idle' else 'Medium' if agent.get('status') == 'active' else 'High'
                }
            
            # Get recent communications
            communications = list(mongo_db['agent_communications'].find().sort('timestamp', -1).limit(50))
            
            return render_template('agents.html',
                                agents=agents_list,
                                agent_metrics=agent_metrics,
                                communications=communications)
        except Exception as e:
            logger.error(f"Error in agents route (MongoDB): {e}")
            return render_template('agents.html',
                                  agents=[],
                                  agent_metrics={},
                                  communications=[],
                                  error=str(e))

    @app.route('/scenarios')
    def scenarios():
        """Scenarios page (MongoDB version)"""
        try:
            # Get all scenarios
            scenarios_list = list(mongo_db['scenarios'].find().sort('created_at', -1))
            
            # Define scenario types for the template
            scenario_types = [
                {
                    'id': 'weather_disruption',
                    'name': 'Weather Disruption',
                    'description': 'Simulate weather-related flight disruptions and delays'
                },
                {
                    'id': 'mechanical_issue',
                    'name': 'Mechanical Issue',
                    'description': 'Test aircraft maintenance and mechanical failure scenarios'
                },
                {
                    'id': 'crew_shortage',
                    'name': 'Crew Shortage',
                    'description': 'Simulate crew scheduling and availability issues'
                },
                {
                    'id': 'airport_closure',
                    'name': 'Airport Closure',
                    'description': 'Test airport resource and facility closure scenarios'
                }
            ]
            
            return render_template('scenarios.html', 
                                 scenarios=scenarios_list,
                                 scenario_types=scenario_types)
        except Exception as e:
            logger.error(f"Error in scenarios route (MongoDB): {e}")
            return render_template('scenarios.html', 
                                 scenarios=[],
                                 scenario_types=[],
                                 error=str(e))

    @app.route('/api/agent_status')
    def agent_status():
        """API endpoint for agent status (MongoDB version)"""
        try:
            agents = list(mongo_db['agents'].find())
            agent_data = []
            for agent in agents:
                agent_data.append({
                    'name': agent['name'],
                    'status': agent.get('status', 'unknown'),
                    'current_task': agent.get('current_task'),
                    'last_activity': agent.get('last_activity')
                })
            return jsonify({
                'success': True,
                'agents': agent_data
            })
        except Exception as e:
            logger.error(f"Error in agent_status API (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/coordinate/<int:disruption_id>', methods=['POST'])
    def coordinate_disruption(disruption_id):
        """API endpoint to coordinate agents for a disruption (MongoDB version)"""
        try:
            if not coordinator:
                return jsonify({'success': False, 'error': 'Agent coordinator not initialized'}), 500
            # Get the disruption from MongoDB
            disruption = mongo_db['disruptions'].find_one({'id': disruption_id})
            if not disruption:
                return jsonify({'success': False, 'error': 'Disruption not found'}), 404
            # Start coordination
            result = coordinator.coordinate_disruption_response(disruption_id)
            return jsonify({
                'success': True,
                'result': result
            })
        except Exception as e:
            logger.error(f"Error in coordinate_disruption API (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/reset_agents', methods=['POST'])
    def reset_agents():
        """API endpoint to reset all agents (MongoDB version)"""
        try:
            update_result = mongo_db['agents'].update_many({}, {'$set': {'status': 'idle', 'current_task': None}})
            logger.info(f"All agents have been reset to IDLE status (MongoDB, matched: {update_result.matched_count})")
            return jsonify({
                'success': True,
                'message': 'All agents have been reset successfully'
            })
        except Exception as e:
            logger.error(f"Error resetting agents (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/start_scenario/<int:scenario_id>', methods=['POST'])
    def start_scenario(scenario_id):
        """API endpoint to start a scenario (MongoDB version)"""
        try:
            scenario = mongo_db['scenarios'].find_one({'id': scenario_id})
            if not scenario:
                return jsonify({'success': False, 'error': 'Scenario not found'}), 404
            # Update scenario status
            mongo_db['scenarios'].update_one({'id': scenario_id}, {'$set': {'status': 'running'}})
            # Start coordination if there's a disruption
            disruption_id = scenario.get('disruption_id')
            if disruption_id and coordinator:
                coordinator.coordinate_disruption_response(disruption_id)
            return jsonify({
                'success': True,
                'message': f"Scenario '{scenario.get('name', 'Unnamed')}' started successfully"
            })
        except Exception as e:
            logger.error(f"Error starting scenario (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    app.add_template_filter(timeago_filter, 'timeago')

    @app.route('/api/create_scenario', methods=['POST'])
    def create_scenario():
        try:
            data = request.get_json()
            # Create new scenario document
            scenario_doc = {
                'id': int(mongo_db['scenarios'].estimated_document_count()) + 1,
                'name': data.get('name', 'Unnamed Scenario'),
                'description': data.get('description', ''),
                'scenario_type': data.get('scenario_type'),
                'parameters': data.get('parameters', {}),
                'status': 'running',
                'created_at': datetime.utcnow().isoformat(),
                'completed_at': None,
                'results': None
            }
            mongo_db['scenarios'].insert_one(scenario_doc)
            # Run scenario simulation
            simulator = DataSimulator()
            scenario_result = simulator.create_test_scenario(scenario_doc['scenario_type'])
            # Update scenario with results
            mongo_db['scenarios'].update_one({'id': scenario_doc['id']}, {'$set': {
                'results': scenario_result,
                'status': 'completed',
                'completed_at': datetime.utcnow().isoformat()
            }})
            return jsonify({
                'success': True,
                'scenario_id': scenario_doc['id'],
                'results': scenario_result
            })
        except Exception as e:
            logger.error(f"Scenario creation error (MongoDB): {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/scenarios')
    def scenarios_api():
        """API endpoint for scenarios (MongoDB version)"""
        try:
            scenarios = list(mongo_db['scenarios'].find().sort('created_at', -1))
            scenarios_data = []
            for scenario in scenarios:
                try:
                    parameters = scenario.get('parameters', {})
                    results = scenario.get('results', {})
                    if isinstance(parameters, str):
                        parameters = json.loads(parameters)
                    if isinstance(results, str):
                        results = json.loads(results)
                except:
                    parameters = {}
                    results = {}
                scenarios_data.append({
                    'id': scenario.get('id'),
                    'name': scenario.get('name'),
                    'description': scenario.get('description'),
                    'scenario_type': scenario.get('scenario_type'),
                    'parameters': parameters,
                    'results': results,
                    'status': scenario.get('status'),
                    'created_at': scenario.get('created_at'),
                    'completed_at': scenario.get('completed_at')
                })
            return jsonify(scenarios_data)
        except Exception as e:
            logger.error(f"Scenarios API error (MongoDB): {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/scenarios/<int:scenario_id>')
    def get_scenario(scenario_id):
        """API endpoint to get scenario details (MongoDB version)"""
        try:
            scenario = mongo_db['scenarios'].find_one({'id': scenario_id})
            if not scenario:
                return jsonify({'success': False, 'error': 'Scenario not found'}), 404
            try:
                parameters = scenario.get('parameters', {})
                results = scenario.get('results', {})
                if isinstance(parameters, str):
                    parameters = json.loads(parameters)
                if isinstance(results, str):
                    results = json.loads(results)
            except:
                parameters = {}
                results = {}
            scenario_data = {
                'id': scenario.get('id'),
                'name': scenario.get('name'),
                'description': scenario.get('description'),
                'scenario_type': scenario.get('scenario_type'),
                'parameters': parameters,
                'results': results,
                'status': scenario.get('status'),
                'created_at': scenario.get('created_at'),
                'completed_at': scenario.get('completed_at')
            }
            return jsonify({'success': True, 'scenario': scenario_data})
        except Exception as e:
            logger.error(f"Error getting scenario {scenario_id} (MongoDB): {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/scenarios/<int:scenario_id>/results')
    def get_scenario_results(scenario_id):
        """API endpoint to get scenario results (MongoDB version)"""
        try:
            scenario = mongo_db['scenarios'].find_one({'id': scenario_id})
            if not scenario:
                return jsonify({'success': False, 'error': 'Scenario not found'}), 404
            try:
                results = scenario.get('results', {})
                if isinstance(results, str):
                    results = json.loads(results)
            except:
                results = {}
            # Generate mock results if none exist
            if not results:
                results = {
                    'response_time': '2.3 seconds',
                    'success_rate': '94.2%',
                    'cost_impact': '15,750',
                    'agent_performance': {
                        'Passenger Rebooking Agent': {'status': 'success', 'tasks_completed': 45},
                        'Crew Scheduling Agent': {'status': 'success', 'tasks_completed': 23},
                        'Aircraft Maintenance Agent': {'status': 'success', 'tasks_completed': 12},
                        'Airport Resource Agent': {'status': 'success', 'tasks_completed': 34},
                        'Customer Communication Agent': {'status': 'success', 'tasks_completed': 67}
                    }
                }
            return jsonify({'success': True, 'results': results})
        except Exception as e:
            logger.error(f"Error getting scenario results {scenario_id} (MongoDB): {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/scenarios/<int:scenario_id>/export')
    def export_scenario_results(scenario_id):
        """API endpoint to export scenario results (MongoDB version)"""
        try:
            scenario = mongo_db['scenarios'].find_one({'id': scenario_id})
            if not scenario:
                return jsonify({'success': False, 'error': 'Scenario not found'}), 404
            try:
                results = scenario.get('results', {})
                if isinstance(results, str):
                    results = json.loads(results)
            except:
                results = {}
            export_data = {
                'scenario_info': {
                    'id': scenario.get('id'),
                    'name': scenario.get('name'),
                    'type': scenario.get('scenario_type'),
                    'created_at': scenario.get('created_at'),
                    'status': scenario.get('status')
                },
                'results': results,
                'export_timestamp': datetime.utcnow().isoformat()
            }
            from flask import Response
            return Response(
                json.dumps(export_data, indent=2),
                mimetype='application/json',
                headers={'Content-Disposition': f'attachment; filename=scenario_{scenario_id}_results.json'}
            )
        except Exception as e:
            logger.error(f"Error exporting scenario results {scenario_id} (MongoDB): {e}")
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/flights')
    def flights_api():
        """API endpoint for flights (MongoDB version)"""
        try:
            flights = list(mongo_db['flights'].find().sort('scheduled_departure', -1).limit(100))
            flights_data = []
            for flight in flights:
                flights_data.append({
                    'id': flight.get('id'),
                    'flight_number': flight.get('flight_number'),
                    'origin': flight.get('origin'),
                    'destination': flight.get('destination'),
                    'scheduled_departure': flight.get('scheduled_departure'),
                    'actual_departure': flight.get('actual_departure'),
                    'scheduled_arrival': flight.get('scheduled_arrival'),
                    'actual_arrival': flight.get('actual_arrival'),
                    'aircraft_id': flight.get('aircraft_id'),
                    'crew_list': flight.get('crew_list'),
                    'passenger_count': flight.get('passenger_count'),
                    'status': flight.get('status'),
                    'delay_minutes': flight.get('delay_minutes'),
                    'disruption_type': flight.get('disruption_type')
                })
            return jsonify(flights_data)
        except Exception as e:
            logger.error(f"Flights API error (MongoDB): {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/disruptions')
    def disruptions_api():
        """API endpoint for disruptions (MongoDB version)"""
        try:
            disruptions = list(mongo_db['disruptions'].find().sort('created_at', -1))
            disruptions_data = []
            for disruption in disruptions:
                disruptions_data.append({
                    'id': disruption.get('id'),
                    'type': disruption.get('type'),
                    'severity': disruption.get('severity'),
                    'description': disruption.get('description'),
                    'affected_flights': disruption.get('affected_flight_list', []),
                    'affected_airports': disruption.get('affected_airport_list', []),
                    'start_time': disruption.get('start_time'),
                    'end_time': disruption.get('end_time'),
                    'estimated_end_time': disruption.get('estimated_end_time'),
                    'status': disruption.get('status'),
                    'created_at': disruption.get('created_at')
                })
            return jsonify(disruptions_data)
        except Exception as e:
            logger.error(f"Disruptions API error (MongoDB): {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/communications/<int:disruption_id>')
    def get_communications(disruption_id):
        """API endpoint to get communications for a specific disruption (MongoDB version)"""
        try:
            # Get communications from MongoDB
            communications = list(mongo_db['agent_communications'].find({'disruption_id': disruption_id}).sort('timestamp', -1).limit(20))
            comm_list = []
            for comm in communications:
                try:
                    content_dict = json.loads(comm.get('content', '{}')) if comm.get('content') else {}
                except:
                    content_dict = {}
                comm_data = {
                    'id': comm.get('id'),
                    'sender': comm.get('sender'),
                    'receiver': comm.get('receiver'),
                    'message_type': comm.get('message_type'),
                    'content': comm.get('content'),
                    'content_dict': content_dict,
                    'timestamp': comm.get('timestamp'),
                    'processed': comm.get('processed')
                }
                comm_list.append(comm_data)
            return jsonify({
                'success': True,
                'communications': comm_list
            })
        except Exception as e:
            logger.error(f"Error getting communications for disruption {disruption_id} (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/communications/recent')
    def get_recent_communications():
        """API endpoint to get recent communications for agent chatter (MongoDB version)"""
        try:
            # Get recent communications from the database
            communications = list(mongo_db['agent_communications'].find().sort('timestamp', -1).limit(10))
            comm_list = []
            for comm in communications:
                try:
                    content_dict = json.loads(comm.get('content', '{}')) if comm.get('content') else {}
                except:
                    content_dict = {}
                comm_data = {
                    'id': comm.get('id'),
                    'sender': comm.get('sender'),
                    'receiver': comm.get('receiver'),
                    'message_type': comm.get('message_type'),
                    'content': comm.get('content'),
                    'content_dict': content_dict,
                    'timestamp': comm.get('timestamp'),
                    'processed': comm.get('processed')
                }
                comm_list.append(comm_data)
            # If no communications in database, return mock data
            if not comm_list:
                comm_list = [
                    {
                        'id': 1,
                        'sender': 'Passenger Rebooking Agent',
                        'receiver': 'Customer Communication Agent',
                        'message_type': 'status_update',
                        'content': 'Processing 15 rebookings for weather disruption',
                        'timestamp': datetime.utcnow().isoformat(),
                        'processed': True
                    },
                    {
                        'id': 2,
                        'sender': 'Crew Scheduling Agent',
                        'receiver': 'Airport Resource Agent',
                        'message_type': 'status_update',
                        'content': 'Duty time compliance check completed',
                        'timestamp': (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                        'processed': True
                    },
                    {
                        'id': 3,
                        'sender': 'Aircraft Maintenance Agent',
                        'receiver': 'Crew Scheduling Agent',
                        'message_type': 'status_update',
                        'content': 'Aircraft inspection scheduled for Gate 15',
                        'timestamp': (datetime.utcnow() - timedelta(minutes=8)).isoformat(),
                        'processed': True
                    },
                    {
                        'id': 4,
                        'sender': 'Customer Communication Agent',
                        'receiver': 'Passenger Rebooking Agent',
                        'message_type': 'status_update',
                        'content': 'Passenger notifications sent - 234 SMS delivered',
                        'timestamp': (datetime.utcnow() - timedelta(minutes=12)).isoformat(),
                        'processed': True
                    }
                ]
            return jsonify({
                'success': True,
                'communications': comm_list
            })
        except Exception as e:
            logger.error(f"Error getting recent communications (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/start_agents', methods=['POST'])
    def start_agents():
        """API endpoint to start all agents (MongoDB version)"""
        try:
            update_result = mongo_db['agents'].update_many({}, {'$set': {'status': 'active', 'current_task': 'Ready for coordination'}})
            logger.info(f"All agents have been started (MongoDB, matched: {update_result.matched_count})")
            return jsonify({
                'success': True,
                'message': 'All agents have been started successfully'
            })
        except Exception as e:
            logger.error(f"Error starting agents (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/pause_agents', methods=['POST'])
    def pause_agents():
        """API endpoint to pause all agents (MongoDB version)"""
        try:
            update_result = mongo_db['agents'].update_many({'status': 'processing'}, {'$set': {'status': 'active', 'current_task': 'Paused'}})
            logger.info(f"All agents with status 'processing' have been paused (MongoDB, matched: {update_result.matched_count})")
            return jsonify({
                'success': True,
                'message': 'All agents have been paused successfully'
            })
        except Exception as e:
            logger.error(f"Error pausing agents (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/agent_config', methods=['POST'])
    def agent_config():
        """API endpoint to save agent configuration"""
        try:
            data = request.get_json()
            agent_name = data.get('agent_name')
            
            # In a real implementation, this would save to a configuration table
            # For now, we'll just log the configuration
            logger.info(f"Agent configuration saved for {agent_name}: {data}")
            
            return jsonify({
                'success': True,
                'message': f'Configuration saved for {agent_name}',
                'config': data
            })
        except Exception as e:
            logger.error(f"Error saving agent configuration: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test_communication', methods=['POST'])
    def test_communication():
        """Test endpoint to create and retrieve a communication record (MongoDB version)"""
        try:
            # Create a test communication record
            test_comm = {
                'id': int(mongo_db['agent_communications'].estimated_document_count()) + 1,
                'sender': 'Test Agent',
                'receiver': 'Test Receiver',
                'message_type': 'test_message',
                'content': '{"test": "data"}',
                'processed': False,
                'disruption_id': 999,
                'timestamp': datetime.utcnow().isoformat()
            }
            mongo_db['agent_communications'].insert_one(test_comm)
            # Retrieve the record
            retrieved_comm = mongo_db['agent_communications'].find_one({'disruption_id': 999, 'sender': 'Test Agent'})
            if retrieved_comm:
                result = {
                    'success': True,
                    'message': 'Test communication created and retrieved successfully',
                    'record_id': retrieved_comm.get('id'),
                    'sender': retrieved_comm.get('sender'),
                    'receiver': retrieved_comm.get('receiver')
                }
            else:
                result = {
                    'success': False,
                    'message': 'Test communication created but not retrieved'
                }
            # Clean up
            mongo_db['agent_communications'].delete_one({'id': test_comm['id']})
            return jsonify(result)
        except Exception as e:
            logger.error(f"Test communication error (MongoDB): {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/create_test_comm/<int:disruption_id>', methods=['POST'])
    def create_test_comm(disruption_id):
        """API endpoint to create a test communication (MongoDB version)"""
        try:
            data = request.get_json() or {}
            test_comm = {
                'id': int(mongo_db['agent_communications'].estimated_document_count()) + 1,
                'sender': data.get('sender', 'Test Agent'),
                'receiver': data.get('receiver', 'Test Receiver'),
                'message_type': data.get('message_type', 'test'),
                'content': json.dumps(data.get('message', {'test': 'data', 'disruption_id': disruption_id})),
                'processed': False,
                'disruption_id': disruption_id,
                'timestamp': datetime.utcnow().isoformat()
            }
            mongo_db['agent_communications'].insert_one(test_comm)
            logger.info(f"Test communication created for disruption {disruption_id} (MongoDB)")
            return jsonify({
                    'success': True,
                'message': 'Test communication created successfully',
                'communication_id': test_comm['id']
            })
        except Exception as e:
            logger.error(f"Error creating test communication (MongoDB): {e}")
            return jsonify({
                    'success': False,
                'error': str(e)
            }), 500

    # New coordination testing endpoints
    @app.route('/api/test/coordination/status')
    def test_system_status():
        """API endpoint to check system status using test utilities"""
        try:
            result = quick_system_check()
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in system status test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test/coordination/quick/<int:disruption_id>')
    def test_quick_coordination(disruption_id):
        """API endpoint for quick coordination test"""
        try:
            result = quick_coordination_test(disruption_id)
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in quick coordination test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test/coordination/communications/<int:disruption_id>')
    def test_communications_persistence(disruption_id):
        """API endpoint for communications persistence test"""
        try:
            result = quick_communications_test(disruption_id)
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in communications test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test/coordination/full', methods=['POST'])
    def test_full_coordination():
        """API endpoint for full coordination test workflow"""
        try:
            data = request.get_json() or {}
            disruption_id = data.get('disruption_id')
            wait_time = data.get('wait_time', 10)
            
            runner = CoordinationTestRunner()
            result = runner.run_full_coordination_test(disruption_id, wait_time)
            
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in full coordination test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test/coordination/agent/<int:disruption_id>')
    def test_agent_coordination_only(disruption_id):
        """API endpoint for agent coordination test only"""
        try:
            runner = CoordinationTestRunner()
            result = runner.test_agent_coordination(disruption_id)
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in agent coordination test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/test/coordination/disruptions')
    def test_get_disruptions():
        """API endpoint to test getting disruptions"""
        try:
            runner = CoordinationTestRunner()
            result = runner.get_existing_disruptions()
            return jsonify(result.to_dict())
        except Exception as e:
            logger.error(f"Error in disruptions test: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/business_metrics/<int:disruption_id>')
    def get_business_metrics(disruption_id):
        """API endpoint to get business metrics for a coordination event"""
        try:
            result = business_metrics_service.get_coordination_business_metrics(disruption_id)
            
            if "error" in result:
                return jsonify({
                    'success': False,
                    'error': result["error"]
                }), 404
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"Error getting business metrics for disruption {disruption_id}: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500

    @app.route('/api/seed_realistic_data', methods=['POST'])
    def seed_realistic_data():
        """Seed database with realistic airline disruption scenarios"""
        try:
            from services.data_simulator import DataSimulator
            simulator = DataSimulator()
            result = simulator.seed_database_with_realistic_scenarios()
            
            return jsonify({
                "success": True,
                "message": "Database seeded with realistic scenarios",
                "data": result
            })
        except Exception as e:
            logging.error(f"Error seeding realistic data: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route('/api/seed_database', methods=['POST'])
    def seed_database():
        """Legacy seed database route - now redirects to realistic seeding"""
        try:
            from services.data_simulator import DataSimulator
            simulator = DataSimulator()
            result = simulator.seed_database_with_realistic_scenarios()
            
            return jsonify({
                "success": True,
                "message": "Database seeded with realistic scenarios",
                "data": result
            })
        except Exception as e:
            logging.error(f"Error seeding database: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    def not_found_error(error):
        return render_template('404.html'), 404
    def internal_error(error):
        return render_template('500.html'), 500
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

def timeago_filter(dt):
    """Convert datetime to human readable time ago format"""
    if not dt:
        return "Never"
    
    now = datetime.utcnow()
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"
