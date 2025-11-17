"""Structured logging for the agent system."""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "analytics_agent",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
) -> logging.Logger:
    """
    Set up structured logger for the agent system.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "analytics_agent") -> logging.Logger:
    """Get or create a logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger

