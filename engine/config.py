ASSISTANT_NAME = "adva"
LLM_KEY = "AIzaSyD3xE7BngtiPhIuOwFjEQnaN_A1aKxPZRM"

# Add after ASSISTANT_NAME

# ==================== API KEYS ==================== #
# Get your API keys from respective services:
# Gemini: https://makersuite.google.com/app/apikey
# Weather: https://openweathermap.org/api
# News: https://newsapi.org/

# Gemini AI API Key (REQUIRED)
LLM_KEY = "AIzaSyD3xE7BngtiPhIuOwFjEQnaN_A1aKxPZRM"

# Weather API Key (Optional)
WEATHER_API_KEY = "cac9cd79103138a8577dd004f224aeec"

# News API Key (Optional)
NEWS_API_KEY = "ae16f11247ac4998aad5658aee96db78"

# ==================== FEATURE FLAGS ==================== #
ENABLE_FACE_AUTH = False
ENABLE_BACKGROUND_MODE = True
ENABLE_NLP = True



"""
Configuration File for AI Desktop Virtual Assistant
Store all API keys, settings, and constants here
"""

# ==================== ASSISTANT CONFIGURATION ==================== #
ASSISTANT_NAME = "Adva"

# ==================== API KEYS ==================== #
# Get your API keys from respective services:
# OpenWeather: https://openweathermap.org/api
# NewsAPI: https://newsapi.org/
# Gemini: https://makersuite.google.com/app/apikey

# Gemini AI API Key (REQUIRED)
LLM_KEY = "AIzaSyD3xE7BngtiPhIuOwFjEQnaN_A1aKxPZRM"

# Weather API Key (Optional)
WEATHER_API_KEY = "cac9cd79103138a8577dd004f224aeec"

# News API Key (Optional)
NEWS_API_KEY = "ae16f11247ac4998aad5658aee96db78"

# ==================== SPEECH SETTINGS ==================== #
SPEECH_RATE = 174  # Words per minute
VOICE_INDEX = 1  # 0 for male, 1 for female (depends on system)

# ==================== RECOGNITION SETTINGS ==================== #
RECOGNITION_TIMEOUT = 10  # seconds
RECOGNITION_PHRASE_LIMIT = 8  # seconds
PAUSE_THRESHOLD = 1  # seconds

# ==================== DATABASE SETTINGS ==================== #
DATABASE_NAME = "adva.db"

# ==================== ANDROID DEVICE SETTINGS ==================== #
DEFAULT_DEVICE_IP = "192.0.0.4"  # Change to your device IP
ADB_PORT = 5555

# ==================== CACHE SETTINGS ==================== #
API_CACHE_TTL = 1800  # seconds (30 minutes)
WEATHER_CACHE_TTL = 1800  # 30 minutes
NEWS_CACHE_TTL = 1800  # 30 minutes
WIKI_CACHE_TTL = 3600  # 1 hour

# ==================== UI SETTINGS ==================== #
WINDOW_SIZE = (1200, 800)
DEFAULT_LOCATION = "Mysuru, Karnataka, IN"

# ==================== LOGGING SETTINGS ==================== #
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "assistant.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ==================== PERFORMANCE SETTINGS ==================== #
MAX_WORKER_THREADS = 3
ENABLE_CACHING = True
ENABLE_PERFORMANCE_MONITORING = True

# ==================== FEATURE FLAGS ==================== #
ENABLE_FACE_AUTH = True
ENABLE_HOTWORD = True
ENABLE_NLP = True
ENABLE_EXTERNAL_APIS = True

# ==================== NLP SETTINGS ==================== #
NLP_CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence for intent recognition
CONTEXT_TIMEOUT = 300  # seconds (5 minutes)

# ==================== CONTACT SETTINGS ==================== #
DEFAULT_COUNTRY_CODE = "+91"  # India

# ==================== YOUTUBE SETTINGS ==================== #
YOUTUBE_SEARCH_LIMIT = 5

# ==================== WEB BROWSER ==================== #
DEFAULT_BROWSER = "msedge"  # Can be 'chrome', 'firefox', 'msedge'

# ==================== GEMINI PROMPT SETTINGS ==================== #
GEMINI_MODEL = "gemini-2.0-flash"
MAX_GEMINI_CONTEXT_LENGTH = 5  # Remember last 5 exchanges

# ==================== SAFETY SETTINGS ==================== #
MAX_MESSAGE_LENGTH = 500  # characters
MAX_COMMAND_RETRY = 3
ERROR_RETRY_DELAY = 2  # seconds

# ==================== HOTWORD DETECTION ==================== #
HOTWORDS = ["jarvis", "adva", "computer"]  # Porcupine wake words
HOTWORD_SENSITIVITY = 0.5

# ==================== SHORTCUTS ==================== #
WAKE_SHORTCUT = "win+j"  # Windows + J to activate

# ==================== VERSION INFO ==================== #
VERSION = "2.0.0"
BUILD_DATE = "2025-11-02"
AUTHOR = "V-Shashwath & Team"

# ==================== DEBUG MODE ==================== #
DEBUG_MODE = False  # Set to True for detailed logging
