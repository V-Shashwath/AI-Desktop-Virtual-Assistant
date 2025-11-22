"""
Utility Functions Module
Common helper functions used across the application
"""

import os
import sys
import time
import psutil
import re
from datetime import datetime, timedelta
from functools import wraps
import logging

logger = logging.getLogger(__name__)


# ==================== PERFORMANCE DECORATORS ==================== #

def timer(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        logger.debug(f"{func.__name__} took {duration:.3f}s")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    """Decorator to retry function on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"{func.__name__} failed (attempt {attempt+1}/{max_attempts}): {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


# ==================== TEXT PROCESSING ==================== #

def clean_text(text):
    """Clean text by removing special characters"""
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def truncate_text(text, max_length=100):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def extract_name_from_query(query, keywords):
    """Extract name after keywords"""
    for keyword in keywords:
        pattern = f'{keyword}\\s+(\\w+)'
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)


# ==================== SYSTEM UTILITIES ==================== #

def get_system_stats():
    """Get current system statistics"""
    try:
        stats = {
            'cpu_percent': psutil.cpu_percent(interval=0.1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'process_count': len(psutil.pids())
        }
        return stats
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        return {}


def get_battery_status():
    """Get battery information"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            return {
                'percent': battery.percent,
                'plugged': battery.power_plugged,
                'time_left': battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
            }
        return None
    except:
        return None


def is_process_running(process_name):
    """Check if a process is running"""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == process_name.lower():
                return True
        return False
    except:
        return False


def kill_process(process_name):
    """Kill a process by name"""
    try:
        os.system(f"taskkill /f /im {process_name}")
        return True
    except:
        return False


# ==================== FILE OPERATIONS ==================== #

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Created directory: {path}")


def read_file_safe(filepath, default=""):
    """Read file with error handling"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Error reading {filepath}: {e}")
        return default


def write_file_safe(filepath, content):
    """Write to file with error handling"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        logger.error(f"Error writing to {filepath}: {e}")
        return False


# ==================== TIME UTILITIES ==================== #

def get_time_of_day():
    """Get time of day (morning, afternoon, evening, night)"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"


def get_greeting():
    """Get appropriate greeting based on time"""
    time_of_day = get_time_of_day()
    greetings = {
        'morning': "Good morning",
        'afternoon': "Good afternoon",
        'evening': "Good evening",
        'night': "Good night"
    }
    return greetings.get(time_of_day, "Hello")


def format_duration(seconds):
    """Format seconds into human-readable duration"""
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        hours = int(seconds / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''}"


def get_relative_time(dt):
    """Get relative time string (e.g., '2 hours ago')"""
    now = datetime.now()
    diff = now - dt
    
    if diff.total_seconds() < 60:
        return "just now"
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(diff.total_seconds() / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


# ==================== VALIDATION ==================== #

def is_valid_email(email):
    """Validate email address"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate phone number (basic check)"""
    phone = re.sub(r'\D', '', phone)  # Remove non-digits
    return 10 <= len(phone) <= 15


def is_valid_url(url):
    """Validate URL"""
    pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
    return re.match(pattern, url) is not None


# ==================== DATA STRUCTURES ==================== #

def safe_dict_get(dictionary, keys, default=None):
    """Safely get nested dictionary value"""
    try:
        for key in keys:
            dictionary = dictionary[key]
        return dictionary
    except (KeyError, TypeError):
        return default


def merge_dicts(*dicts):
    """Merge multiple dictionaries"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


# ==================== STRING UTILITIES ==================== #

def similarity_ratio(str1, str2):
    """Calculate similarity between two strings (0-1)"""
    str1, str2 = str1.lower(), str2.lower()
    if str1 == str2:
        return 1.0
    
    # Simple character-based similarity
    set1, set2 = set(str1), set(str2)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union if union > 0 else 0.0


def fuzzy_match(query, options, threshold=0.6):
    """Find best match from options using fuzzy matching"""
    best_match = None
    best_score = 0
    
    for option in options:
        score = similarity_ratio(query, option)
        if score > best_score and score >= threshold:
            best_score = score
            best_match = option
    
    return best_match, best_score


def format_list_natural(items):
    """Format list naturally (e.g., 'a, b, and c')"""
    if not items:
        return ""
    if len(items) == 1:
        return str(items[0])
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(str(i) for i in items[:-1])}, and {items[-1]}"


# ==================== CACHING ==================== #

_simple_cache = {}

def cache_set(key, value, ttl=3600):
    """Set value in simple cache"""
    expiry = time.time() + ttl
    _simple_cache[key] = (value, expiry)


def cache_get(key):
    """Get value from simple cache"""
    if key in _simple_cache:
        value, expiry = _simple_cache[key]
        if time.time() < expiry:
            return value
        else:
            del _simple_cache[key]
    return None


def cache_clear():
    """Clear all cached values"""
    _simple_cache.clear()


# ==================== ERROR HANDLING ==================== #

def safe_execute(func, *args, default=None, **kwargs):
    """Execute function safely and return default on error"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {e}")
        return default


# ==================== INITIALIZATION ==================== #

def check_dependencies():
    """Check if all required dependencies are installed"""
    required = ['speech_recognition', 'pyttsx3', 'eel', 'nltk', 'requests', 
                'psutil', 'opencv-python', 'pywhatkit', 'pyautogui']
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.warning(f"Missing packages: {', '.join(missing)}")
        return False
    return True


def get_app_version():
    """Get application version info"""
    from engine.config import VERSION, BUILD_DATE
    return {
        'version': VERSION,
        'build_date': BUILD_DATE
    }