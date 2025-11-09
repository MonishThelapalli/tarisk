"""Main entry point for the application."""

import sys
import json
import asyncio
from dotenv import load_dotenv
import logging
from hypercorn.config import Config
from hypercorn.asyncio import serve

from config.settings import get_database_connection_string
from managers.scheduler import WorkflowScheduler
from api.app import app

# Load environment variables
load_dotenv()

# Basic logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

async def run_server():
    """Run the server using hypercorn."""
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    config.accesslog = None
    config.errorlog = None
    await serve(app, config)

def main():
    """Main function."""
    # Parse command line arguments
    if len(sys.argv) > 1:
        connection_string = get_database_connection_string()
        
        if sys.argv[1] == "--workflow-only":
            workflow_scheduler = WorkflowScheduler(connection_string)
            result = workflow_scheduler.run_now()
            print(json.dumps(result, indent=2))
            return
        
        elif sys.argv[1] == "--scheduler-only":
            workflow_scheduler = WorkflowScheduler(connection_string)
            workflow_scheduler.start()
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                workflow_scheduler.stop()
                print("Scheduler stopped")
            return
    
    # Run the API server
    try:
        logger.info("Starting server at http://127.0.0.1:8000")
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.info("Shutting down server")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()
