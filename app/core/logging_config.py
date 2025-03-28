from loguru import logger
import sys

# Configure loguru
logger.remove()  # Remove default logger
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    colorize=True,
    backtrace=True,
    diagnose=True,
)

# Optional: Add a file-based logger
logger.add(
    "logs/app.log",
    rotation="1 MB",  # Rotate log file when it reaches 1 MB
    retention="7 days",  # Keep logs for 7 days
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)