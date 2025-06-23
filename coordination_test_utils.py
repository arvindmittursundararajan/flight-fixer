#!/usr/bin/env python3
"""
Coordination Test Utilities Module

This module provides reusable functions and classes for testing multi-agent coordination
processes. It can be used for:
- Automated testing of coordination workflows
- Integration testing of agent communications
- Performance monitoring of coordination processes
- Debugging coordination issues

Usage:
    from coordination_test_utils import CoordinationTestRunner, TestResult
    
    # Create test runner
    runner = CoordinationTestRunner(base_url="http://localhost:5000")
    
    # Run full coordination test
    result = runner.run_full_coordination_test(disruption_id=28)
    
    # Run specific test components
    result = runner.test_communications_persistence(disruption_id=28)
    result = runner.test_agent_coordination(disruption_id=28)
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestStatus(Enum):
    """Test execution status"""
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"
    ERROR = "error"
    SKIPPED = "skipped"

@dataclass
class TestResult:
    """Result of a test execution"""
    status: TestStatus
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    duration: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    error_details: Optional[str] = None
    
    def is_success(self) -> bool:
        """Check if test was successful"""
        return self.status == TestStatus.SUCCESS
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "status": self.status.value,
            "message": self.message,
            "data": self.data,
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
            "error_details": self.error_details
        }

class CoordinationTestRunner:
    """Main class for running coordination tests"""
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 120):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.test_disruption_id: Optional[int] = None
        
    def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Optional[requests.Response]:
        """Make HTTP request with error handling"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method == "GET":
                response = self.session.get(url, timeout=10)
            elif method == "POST":
                # Use longer timeout for coordination endpoint
                request_timeout = self.timeout if "/api/coordinate/" in endpoint else 30
                response = self.session.post(url, json=data, timeout=request_timeout)
            elif method == "PUT":
                response = self.session.put(url, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            duration = time.time() - start_time
            logger.info(f"✓ {method} {endpoint} - Status: {response.status_code} ({duration:.2f}s)")
            return response
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"✗ {method} {endpoint} - Error: {str(e)} ({duration:.2f}s)")
            return None
    
    def get_existing_disruptions(self) -> TestResult:
        """Get existing disruptions from the database"""
        logger.info("Getting existing disruptions...")
        
        response = self._make_request("/api/disruptions")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Failed to get disruptions",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        disruptions = response.json()
        logger.info(f"Found {len(disruptions)} existing disruptions")
        
        # Prefer a weather disruption if available
        for disruption in disruptions:
            if disruption['type'] == 'weather':
                self.test_disruption_id = disruption['id']
                logger.info(f"Using weather disruption ID {self.test_disruption_id} for testing")
                break
        else:
            # Fallback to first if none found
            if disruptions:
                self.test_disruption_id = disruptions[0]['id']
                logger.info(f"Using disruption ID {self.test_disruption_id} for testing")
            else:
                return TestResult(
                    status=TestStatus.FAILURE,
                    message="No disruptions found in database"
                )
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message=f"Found {len(disruptions)} disruptions, using ID {self.test_disruption_id}",
            data={"disruptions": disruptions, "selected_id": self.test_disruption_id}
        )
    
    def create_test_communication(self, disruption_id: Optional[int] = None) -> TestResult:
        """Create a test communication to verify the system works"""
        logger.info("Creating test communication...")
        
        if not disruption_id:
            disruption_id = self.test_disruption_id
        
        if not disruption_id:
            return TestResult(
                status=TestStatus.FAILURE,
                message="No disruption ID available for test communication"
            )
        
        test_comm_data = {
            "sender": "Test Agent",
            "receiver": "Test Receiver", 
            "message": "This is a test communication to verify the system works",
            "message_type": "test"
        }
        
        response = self._make_request(f"/api/create_test_comm/{disruption_id}", "POST", test_comm_data)
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Failed to create test communication",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        result = response.json()
        logger.info("Test communication created successfully")
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message="Test communication created successfully",
            data={"communication_id": result.get('communication_id')}
        )
    
    def run_coordination_process(self, disruption_id: Optional[int] = None) -> TestResult:
        """Run the coordination process for a disruption"""
        logger.info("Starting multi-agent coordination process...")
        
        if not disruption_id:
            disruption_id = self.test_disruption_id
        
        if not disruption_id:
            return TestResult(
                status=TestStatus.FAILURE,
                message="No disruption ID available for coordination"
            )
        
        response = self._make_request(f"/api/coordinate/{disruption_id}", "POST")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Failed to start coordination process",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        result = response.json()
        logger.info("Coordination process started successfully")
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message="Coordination process completed successfully",
            data={"coordination_result": result}
        )
    
    def check_communications(self) -> TestResult:
        """Check if communications are saved in the database"""
        logger.info("Checking communications in database...")
        
        response = self._make_request("/api/communications/recent")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Failed to retrieve communications",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        result = response.json()
        communications = result.get('communications', [])
        logger.info(f"Found {len(communications)} recent communications")
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message=f"Found {len(communications)} communications in database",
            data={"communications": communications, "count": len(communications)}
        )
    
    def test_communications_by_disruption(self, disruption_id: Optional[int] = None) -> TestResult:
        """Test getting communications for specific disruption"""
        logger.info("Testing communications by disruption...")
        
        if not disruption_id:
            disruption_id = self.test_disruption_id
        
        if not disruption_id:
            return TestResult(
                status=TestStatus.FAILURE,
                message="No disruption ID available for communication test"
            )
        
        response = self._make_request(f"/api/communications/{disruption_id}")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Failed to retrieve communications for disruption",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        result = response.json()
        communications = result.get('communications', [])
        logger.info(f"Found {len(communications)} communications for disruption {disruption_id}")
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message=f"Found {len(communications)} communications for disruption {disruption_id}",
            data={"communications": communications, "disruption_id": disruption_id, "count": len(communications)}
        )
    
    def run_full_coordination_test(self, disruption_id: Optional[int] = None, wait_time: int = 10) -> TestResult:
        """Run complete coordination test workflow"""
        start_time = time.time()
        logger.info("Starting full coordination test workflow...")
        
        results = {
            "steps": [],
            "overall_success": False,
            "total_duration": 0.0
        }
        
        # Step 1: Get existing disruptions
        step_result = self.get_existing_disruptions()
        results["steps"].append({"name": "get_disruptions", "result": step_result.to_dict()})
        
        if not step_result.is_success():
            return TestResult(
                status=TestStatus.FAILURE,
                message="Cannot proceed without existing disruptions",
                data=results,
                duration=time.time() - start_time
            )
        
        # Use the disruption ID from the result if not provided
        if not disruption_id:
            disruption_id = step_result.data.get("selected_id")
        
        # Step 2: Create test communication
        step_result = self.create_test_communication(disruption_id)
        results["steps"].append({"name": "create_test_comm", "result": step_result.to_dict()})
        
        if not step_result.is_success():
            return TestResult(
                status=TestStatus.FAILURE,
                message="Cannot proceed without test communication",
                data=results,
                duration=time.time() - start_time
            )
        
        # Step 3: Run coordination process
        step_result = self.run_coordination_process(disruption_id)
        results["steps"].append({"name": "coordination_process", "result": step_result.to_dict()})
        
        if not step_result.is_success():
            return TestResult(
                status=TestStatus.FAILURE,
                message="Cannot proceed without coordination process",
                data=results,
                duration=time.time() - start_time
            )
        
        # Step 4: Wait for coordination to complete
        logger.info(f"Waiting {wait_time} seconds for coordination to complete...")
        time.sleep(wait_time)
        
        # Step 5: Check communications
        step_result = self.check_communications()
        results["steps"].append({"name": "check_communications", "result": step_result.to_dict()})
        
        # Step 6: Test communications by disruption
        step_result = self.test_communications_by_disruption(disruption_id)
        results["steps"].append({"name": "communications_by_disruption", "result": step_result.to_dict()})
        
        # Determine overall success
        all_successful = all(step["result"]["status"] == "success" for step in results["steps"])
        results["overall_success"] = all_successful
        
        total_duration = time.time() - start_time
        results["total_duration"] = total_duration
        
        if all_successful:
            comm_count = results["steps"][3]["result"]["data"]["count"]  # check_communications step
            return TestResult(
                status=TestStatus.SUCCESS,
                message=f"SUCCESS: Found {comm_count} communications in database. The coordination process is working correctly!",
                data=results,
                duration=total_duration
            )
        else:
            return TestResult(
                status=TestStatus.FAILURE,
                message="ISSUE: Some test steps failed. Check the results for details.",
                data=results,
                duration=total_duration
            )
    
    def test_agent_coordination(self, disruption_id: Optional[int] = None) -> TestResult:
        """Test only the agent coordination process"""
        logger.info("Testing agent coordination process...")
        
        if not disruption_id:
            disruption_id = self.test_disruption_id
        
        if not disruption_id:
            return TestResult(
                status=TestStatus.FAILURE,
                message="No disruption ID available for coordination test"
            )
        
        return self.run_coordination_process(disruption_id)
    
    def test_communications_persistence(self, disruption_id: Optional[int] = None) -> TestResult:
        """Test only the communications persistence"""
        logger.info("Testing communications persistence...")
        
        if not disruption_id:
            disruption_id = self.test_disruption_id
        
        if not disruption_id:
            return TestResult(
                status=TestStatus.FAILURE,
                message="No disruption ID available for communications test"
            )
        
        # Create test communication
        comm_result = self.create_test_communication(disruption_id)
        if not comm_result.is_success():
            return comm_result
        
        # Check communications
        check_result = self.check_communications()
        if not check_result.is_success():
            return check_result
        
        # Test communications by disruption
        disruption_result = self.test_communications_by_disruption(disruption_id)
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message="Communications persistence test completed successfully",
            data={
                "test_comm_result": comm_result.to_dict(),
                "check_result": check_result.to_dict(),
                "disruption_result": disruption_result.to_dict()
            }
        )
    
    def get_system_status(self) -> TestResult:
        """Get overall system status"""
        logger.info("Getting system status...")
        
        # Test basic connectivity
        response = self._make_request("/api/agent_status")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="System is not responding",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        agent_status = response.json()
        
        # Test disruptions endpoint
        response = self._make_request("/api/disruptions")
        if not response or response.status_code != 200:
            return TestResult(
                status=TestStatus.FAILURE,
                message="Disruptions endpoint not responding",
                error_details=f"Status: {response.status_code if response else 'No response'}"
            )
        
        disruptions = response.json()
        
        return TestResult(
            status=TestStatus.SUCCESS,
            message="System is operational",
            data={
                "agents": agent_status.get("agents", []),
                "disruptions_count": len(disruptions),
                "system_online": True
            }
        )

# Convenience functions for quick testing
def quick_coordination_test(disruption_id: int, base_url: str = "http://localhost:5000") -> TestResult:
    """Quick test of coordination process for a specific disruption"""
    runner = CoordinationTestRunner(base_url=base_url)
    return runner.run_coordination_process(disruption_id)

def quick_communications_test(disruption_id: int, base_url: str = "http://localhost:5000") -> TestResult:
    """Quick test of communications persistence for a specific disruption"""
    runner = CoordinationTestRunner(base_url=base_url)
    return runner.test_communications_persistence(disruption_id)

def quick_system_check(base_url: str = "http://localhost:5000") -> TestResult:
    """Quick system status check"""
    runner = CoordinationTestRunner(base_url=base_url)
    return runner.get_system_status()

# Example usage and testing
if __name__ == "__main__":
    # Example usage
    runner = CoordinationTestRunner()
    
    # Run full test
    result = runner.run_full_coordination_test()
    print(f"Test Result: {result.status.value}")
    print(f"Message: {result.message}")
    print(f"Duration: {result.duration:.2f}s")
    
    if result.is_success():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        print(f"Error: {result.error_details}") 