from loguru import logger
import sys
from typing import Any, Optional
import json

class Colors:
    RESET = "\033[0m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BLUE = "\033[34m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

def format_message(message: Any) -> str:
    try:
        if isinstance(message, (dict, list)):
            return json.dumps(message)
        if hasattr(message, 'dict'):
            return json.dumps(message.dict())
        return str(message)
    except:
        return str(message)

class ServiceLogger:
    def __init__(self, name: str, request_id: Optional[str] = None):
        self.name = name
        self.request_id = request_id

    def input(self, message: Any) -> None:
        logger.info(
            f"{self.name} INPUT ##: {format_message(message)}",
            extra={"request_id": self.request_id}
        )

    def output(self, message: Any, error: Any = None) -> None:
        if error:
            logger.error(
                f"{self.name} OUTPUT_ERROR ##: {format_message(error)}",
                extra={"request_id": self.request_id}
            )
        else:
            logger.info(
                f"{self.name} OUTPUT ##: {format_message(message)}",
                extra={"request_id": self.request_id}
            )

    def debug(self, message: Any) -> None:
        logger.debug(
            f"{self.name} DEBUG ##: {format_message(message)}",
            extra={"request_id": self.request_id}
        )

def create_logger(name: str, request_id: Optional[str] = None) -> ServiceLogger:
    return ServiceLogger(name, request_id)

# Configure logger with format
logger.configure(handlers=[{
    "sink": sys.stdout,
    "colorize": True,
    "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[request_id]} | {message}"
}])

# Remove default logger and add contextualized logger
logger.remove()
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {extra[request_id]} | {message}",
)
