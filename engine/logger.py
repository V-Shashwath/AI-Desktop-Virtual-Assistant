"""
Centralized Logging Module
Provides consistent logging across all modules
"""

import logging
import os
from datetime import datetime
from engine.config import LOG_LEVEL, LOG_FILE, LOG_FORMAT, DEBUG_MODE

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure logging
log_file_path = os.path.join('logs', LOG_FILE)

# Set log level
level = logging.DEBUG if DEBUG_MODE else getattr(logging, LOG_LEVEL.upper(), logging.INFO)

# Create formatter
formatter = logging.Formatter(LOG_FORMAT)

# File handler
file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
file_handler.setLevel(level)
file_handler.setFormatter(formatter)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(level)
console_handler.setFormatter(formatter)

# Create root logger
root_logger = logging.getLogger()
root_logger.setLevel(level)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)


def get_logger(name):
    """Get a logger for a specific module"""
    return logging.getLogger(name)


def log_command(query, intent, confidence):
    """Log user command with intent"""
    logger = get_logger('commands')
    logger.info(f"Query: '{query}' | Intent: {intent} | Confidence: {confidence:.2f}")


def log_api_call(api_name, status, response_time=None):
    """Log external API calls"""
    logger = get_logger('api')
    time_str = f" | Response time: {response_time:.2f}s" if response_time else ""
    logger.info(f"API: {api_name} | Status: {status}{time_str}")


def log_error(module, error, query=None):
    """Log errors with context"""
    logger = get_logger('errors')
    query_str = f" | Query: '{query}'" if query else ""
    logger.error(f"Module: {module} | Error: {str(error)}{query_str}")


def log_performance(operation, duration):
    """Log performance metrics"""
    logger = get_logger('performance')
    logger.info(f"Operation: {operation} | Duration: {duration:.3f}s")


def log_session_start():
    """Log session start"""
    logger = get_logger('session')
    logger.info("="*50)
    logger.info(f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*50)


def log_session_end():
    """Log session end"""
    logger = get_logger('session')
    logger.info("="*50)
    logger.info(f"Session ended at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*50)


# Initialize logging
log_session_start()