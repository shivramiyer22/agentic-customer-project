"""
Logging configuration
"""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = __name__,
    level: Optional[int] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """
    Set up and return a logger instance
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        format_string: Custom format string
        
    Returns:
        Configured logger instance
    """
    if level is None:
        level = logging.INFO
    
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "[%(filename)s:%(lineno)d] - %(message)s"
        )
    
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(format_string)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger


# Default application logger
app_logger = setup_logger("aerospace_customer_service")

