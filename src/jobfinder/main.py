#!/usr/bin/env python
import sys
import warnings

from jobfinder.crew import Jobfinder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information.

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'AI LLMs'
    }
    Jobfinder().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Jobfinder().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Jobfinder().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Jobfinder().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_task():
    """
    Run a specific task using its task ID.
    """
    try:
        task_id = sys.argv[1]  # Get the task ID from the command-line arguments
        print(f"Running task: {task_id}")

        # Provide dynamic inputs for the task
        inputs = {
            # task_id: {
            #     "additional_input": "value"  # Replace with task-specific inputs
            # }
        }

        # Run the task using kickoff (as individual task execution is not supported)
        crew = Jobfinder().crew()
        result = crew.kickoff(inputs=inputs)

        # Display the results
        print(f"Result for task '{task_id}':")
        print(result)

    except Exception as e:
        raise Exception(f"An error occurred while running the task: {e}")
