"""Test module for agent creation and configuration in the JobFinder system."""

import pytest
from unittest.mock import patch, MagicMock
from jobfinder.crew import Jobfinder, AgentConfigError, TaskConfigError
from crewai.project.crew_base import CrewBase

class TestJobfinder(Jobfinder):
    """Test double for Jobfinder that prevents automatic initialization."""
    def __init__(self, *args, **kwargs):
        # Skip the parent's __init__ to prevent automatic initialization
        pass
        
    def map_all_task_variables(self):
        """Override to prevent automatic mapping."""
        pass
        
    def map_all_agent_variables(self):
        """Override to prevent automatic mapping."""
        pass

@pytest.fixture
def mock_crew():
    """Create a test instance with controlled initialization."""
    crew = TestJobfinder()
    crew.agents_config = {}
    crew.tasks_config = {}
    return crew

def test_agent_validation(mock_crew):
    """Test agent configuration validation."""
    # Test valid config
    valid_config = {
        'role': 'Test Agent',
        'goal': 'Test Goal',
        'backstory': 'Test Backstory'
    }
    mock_crew._validate_agent_config(valid_config)  # Should not raise
    
    # Test missing fields
    invalid_config = {
        'role': 'Test Agent',
        # Missing goal and backstory
    }
    with pytest.raises(AgentConfigError) as exc_info:
        mock_crew._validate_agent_config(invalid_config)
    assert "Missing or empty required fields" in str(exc_info.value)
    assert "goal" in str(exc_info.value)
    assert "backstory" in str(exc_info.value)

def test_task_validation(mock_crew):
    """Test task configuration validation."""
    # Test valid config
    valid_config = {
        'description': 'Test Task',
        'expected_output': 'Test Output',
        'agent': 'test_agent'
    }
    mock_crew._validate_task_config(valid_config)  # Should not raise
    
    # Test missing fields
    invalid_config = {
        'description': 'Test Task',
        # Missing expected_output and agent
    }
    with pytest.raises(TaskConfigError) as exc_info:
        mock_crew._validate_task_config(invalid_config)
    assert "Missing or empty required fields" in str(exc_info.value)
    assert "expected_output" in str(exc_info.value)
    assert "agent" in str(exc_info.value)

def test_agent_creation_error_handling(mock_crew):
    """Test error handling during agent creation."""
    with patch('jobfinder.crew.Agent', side_effect=Exception("Agent creation failed")):
        mock_crew.agents_config = {
            'job_searcher': {
                'role': 'Test Agent',
                'goal': 'Test Goal',
                'backstory': 'Test Backstory'
            }
        }
        
        with pytest.raises(AgentConfigError) as exc_info:
            mock_crew.job_searcher()
        assert "Error creating job_searcher agent" in str(exc_info.value)
        assert "Agent creation failed" in str(exc_info.value)

def test_task_creation_error_handling(mock_crew):
    """Test error handling during task creation."""
    with patch('jobfinder.crew.Task', side_effect=Exception("Task creation failed")):
        mock_crew.tasks_config = {
            'search_jobs': {
                'description': 'Test Task',
                'expected_output': 'Test Output',
                'agent': 'test_agent'
            }
        }
        
        with pytest.raises(TaskConfigError) as exc_info:
            mock_crew.search_jobs()
        assert "Error creating search_jobs task" in str(exc_info.value)
        assert "Task creation failed" in str(exc_info.value)
