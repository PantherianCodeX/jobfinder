"""JobFinder crew implementation for finding and processing job postings.

This module implements the core JobFinder crew using the CrewAI framework.
It defines the essential agents and tasks needed for the MVP job finding system.
"""

from typing import List, Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


class JobFinderError(Exception):
    """Base exception class for JobFinder errors."""
    pass


class AgentConfigError(JobFinderError):
    """Raised when there is an error in agent configuration."""
    pass


class TaskConfigError(JobFinderError):
    """Raised when there is an error in task configuration."""
    pass


@CrewBase
class Jobfinder():
    """Jobfinder crew for finding and processing job postings.
    
    This class implements the core MVP functionality for the job finding system,
    including agent creation, task definition, and crew assembly.
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def _validate_agent_config(self, config: Dict[str, Any]) -> None:
        """Validate agent configuration has required fields.
        
        Args:
            config: Agent configuration dictionary
            
        Raises:
            AgentConfigError: If required fields are missing
        """
        required_fields = ['role', 'goal', 'backstory']
        missing = [field for field in required_fields if not config.get(field)]
        if missing:
            raise AgentConfigError(f"Missing or empty required fields: {missing}")

    def _validate_task_config(self, config: Dict[str, Any]) -> None:
        """Validate task configuration has required fields.
        
        Args:
            config: Task configuration dictionary
            
        Raises:
            TaskConfigError: If required fields are missing
        """
        required_fields = ['description', 'expected_output', 'agent']
        missing = [field for field in required_fields if not config.get(field)]
        if missing:
            raise TaskConfigError(f"Missing or empty required fields: {missing}")

    @agent
    def job_searcher(self) -> Agent:
        """Create and configure the job search specialist agent.
        
        Returns:
            Agent: Configured job search agent
            
        Raises:
            AgentConfigError: If agent configuration is invalid
        """
        try:
            config = self.agents_config['job_searcher']
            self._validate_agent_config(config)
            return Agent(
                config=config,
                verbose=True
            )
        except KeyError as e:
            raise AgentConfigError(f"Missing job_searcher configuration: {e}")
        except AgentConfigError:
            raise
        except Exception as e:
            raise AgentConfigError(f"Error creating job_searcher agent: {e}")

    @agent
    def data_processor(self) -> Agent:
        """Create and configure the data processing specialist agent.
        
        Returns:
            Agent: Configured data processing agent
            
        Raises:
            AgentConfigError: If agent configuration is invalid
        """
        try:
            config = self.agents_config['data_processor']
            self._validate_agent_config(config)
            return Agent(
                config=config,
                verbose=True
            )
        except KeyError as e:
            raise AgentConfigError(f"Missing data_processor configuration: {e}")
        except AgentConfigError:
            raise
        except Exception as e:
            raise AgentConfigError(f"Error creating data_processor agent: {e}")

    @task
    def search_jobs(self) -> Task:
        """Create the job search task.
        
        Returns:
            Task: Configured job search task
            
        Raises:
            TaskConfigError: If task configuration is invalid
        """
        try:
            config = self.tasks_config['search_jobs']
            self._validate_task_config(config)
            return Task(
                config=config
            )
        except KeyError as e:
            raise TaskConfigError(f"Missing search_jobs task configuration: {e}")
        except TaskConfigError:
            raise
        except Exception as e:
            raise TaskConfigError(f"Error creating search_jobs task: {e}")

    @task
    def process_data(self) -> Task:
        """Create the data processing task.
        
        Returns:
            Task: Configured data processing task
            
        Raises:
            TaskConfigError: If task configuration is invalid
        """
        try:
            config = self.tasks_config['process_data']
            self._validate_task_config(config)
            return Task(
                config=config
            )
        except KeyError as e:
            raise TaskConfigError(f"Missing process_data task configuration: {e}")
        except TaskConfigError:
            raise
        except Exception as e:
            raise TaskConfigError(f"Error creating process_data task: {e}")

    @crew
    def crew(self) -> Crew:
        """Initialize and return the job finder crew.
        
        Returns:
            Crew: Configured job finder crew with all agents and tasks
            
        Raises:
            JobFinderError: If crew creation fails
        """
        try:
            return Crew(
                agents=[
                    self.job_searcher(),
                    self.data_processor()
                ],
                tasks=[
                    self.search_jobs(),
                    self.process_data()
                ],
                verbose=True
            )
        except (AgentConfigError, TaskConfigError) as e:
            raise JobFinderError(f"Error creating crew: {e}")
        except Exception as e:
            raise JobFinderError(f"Unexpected error creating crew: {e}")
