
import sys
import logging
from src.agents.orchestration_agent.workflow_manager import WorkflowManager
from src.utils.config_loader import ConfigLoader

def main():
    # Configure logging from environment or default
    config = ConfigLoader.load_config()
    logging.basicConfig(level=config.get("log_level", "INFO"), format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Starting Mechanical Agentic AI application...")

    # Initialize the orchestrator
    orchestrator = WorkflowManager(config=config)

    # Example: Process command line arguments to determine the task
    task_args = sys.argv[1:] # Get arguments passed after 'main.py'

    if not task_args:
        logging.warning("No task specified. Use 'python main.py <task_type> [params]'")
        # Optionally, could run a default or interactive mode
        # orchestrator.run_default_task()
        return

    task_type = task_args[0]
    task_params = {}
    # Simple parsing for key-value pairs like: --key value
    for i in range(1, len(task_args), 2):
        if i + 1 < len(task_args) and task_args[i].startswith('--'):
            key = task_args[i].lstrip('--')
            value = task_args[i+1]
            task_params[key] = value
        else:
            logging.warning(f"Skipping malformed argument: {task_args[i]}")

    logging.info(f"Executing task: {task_type} with parameters: {task_params}")
    try:
        result = orchestrator.execute_task(task_type, task_params)
        logging.info(f"Task '{task_type}' completed. Result: {result}")
    except NotImplementedError as nie:
        logging.error(nie)
    except Exception as e:
        logging.error(f"An error occurred during task execution: {e}", exc_info=True)

if __name__ == "__main__":
    main()
