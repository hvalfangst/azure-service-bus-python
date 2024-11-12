from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic_settings import BaseSettings
from client.logger import logger

load_dotenv()

CONFIG_FILE = "service_bus_config.env"


class ServiceBusConfiguration(BaseSettings):
    CONNECTION_STRING: str
    QUEUE_NAME: str

    class Config:
        env_file = f"client/{CONFIG_FILE}"


def initialize():
    try:
        # Create an instance of ServiceBusConfiguration
        settings = ServiceBusConfiguration()

        # Check if the connection string field is set
        if not settings.CONNECTION_STRING:
            logger.error("Connection string is missing from .env file")
            raise HTTPException(status_code=500, detail="Connection string is missing from .env file")

        # Check if the queue name field is set
        if not settings.QUEUE_NAME:
            logger.error("Queue name is missing from .env file")
            raise HTTPException(status_code=500, detail="Queue name is missing from .env file")

        logger.info("Configuration values loaded successfully.")
        return settings

    # Handle errors (most likely due to file not found)
    except FileNotFoundError:
        logger.critical(f"{CONFIG_FILE} file not found under client directory.")
        raise HTTPException(status_code=500, detail=f"{CONFIG_FILE} file not found under client directory.")
    except Exception as e:
        logger.critical(f"Error loading config: {e}")
        raise HTTPException(status_code=500, detail="Configuration error")


# Initialize ServiceBusConfiguration
config = initialize()
