"""
Enhanced External API Handler - FIXED NEWS
Manages Weather, News, and other external API calls
Wikipedia removed - all queries now go to Gemini AI
NEWS FIXED: Better error handling and response formatting
"""

import requests
import json
from datetime import datetime, timedelta
import logging
import time
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_api_cache = {}
_cache_ttl = {}

try:
    from engine.config import WEATHER_API_KEY, NEWS_API_KEY
except:
    WEATHER_API_KEY = None
    NEWS_API_KEY = None
    logger.warning("API keys not found in config. Some features may not work.")


def cache_response(key, data, ttl_seconds=1800):
    """Cache API response with TTL"""
    global _api_cache, _cache_ttl
    _api_cache[key] = data
    _cache_ttl[key] = time.time() + ttl_seconds


def get_cached_response(key):
    """Get cached response if valid"""
    global _api_cache, _cache_ttl
    if key in _api_cache and key in _cache_ttl:
        if time.time() < _cache_ttl[key]:
            logger.info(f"Cache hit: {key}")
            return _api_cache[key]
        else:
            if key in _api_cache:
                del _api_cache[key]
            if key in _cache_ttl:
                del _cache_ttl[key]
    return None


def clear_cache():
    """Clear all cached responses"""
    global _api_cache, _cache_ttl
    _api_cache.clear()
    _cache_ttl.clear()
    logger.info("API cache cleared")


# ==================== WEATHER API ====================

def get_weather(city="Bengaluru"):
    """Get current weather for a city"""
    cache_key = f"weather_{city}"
    cached = get_cached_response(cache_key)
    if cached:
        return cached
    
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        logger.warning("Weather API key not configured")
        return "Weather service is not configured. Please add your OpenWeather API key in config.py"
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        wind_speed = round(data['wind']['speed'], 1)
        
        result = (f"The current weather in {city} is {temp} degrees Celsius "
                 f"with {description}. It feels like {feels_like} degrees. "
                 f"Humidity is at {humidity} percent and wind speed is {wind_speed} meters per second.")
        
        cache_response(cache_key, result, 1800)
        logger.info(f"Weather data fetched for {city}")
        return result
        
    except requests.exceptions.Timeout:
        logger.error("Weather API timeout")
        return "Weather service is taking too long. Please try again."
    except requests.exceptions.HTTPError as e:
        logger.error(f"Weather API HTTP error: {e}")
        if e.response.status_code == 404:
            return f"City '{city}' not found. Please check the spelling."
        return "Could not fetch weather data. Please try again."
    except Exception as e:
        logger.error(f"Weather error: {e}")
        return "I encountered an error while getting weather information."


def get_weather_forecast(city="Bengaluru", days=3):
    """Get weather forecast for next few days"""
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return "Weather forecast service is not configured."
    
    try:
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric',
            'cnt': days * 8
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        forecasts = []
        seen_dates = set()
        
        for item in data['list']:
            date = item['dt_txt'].split()[0]
            if date not in seen_dates:
                forecasts.append({
                    'date': date,
                    'temp': round(item['main']['temp']),
                    'description': item['weather'][0]['description'].title()
                })
                seen_dates.add(date)
                if len(forecasts) >= days:
                    break
        
        result = f"Weather forecast for {city}: "
        for fc in forecasts:
            result += f"{fc['date']}: {fc['temp']}°C, {fc['description']}. "
        
        cache_response(f"forecast_{city}", result, 1800)
        return result
        
    except Exception as e:
        logger.error(f"Forecast error: {e}")
        return "I couldn't fetch the weather forecast right now."


# ==================== NEWS API - FIXED ====================

def get_news_headlines(country="in", category=None, location=None, count=5):
    """
    Get top news headlines - FIXED version
    """
    cache_key = f"news_{country}_{category}_{location}"
    cached = get_cached_response(cache_key)
    if cached:
        return cached
    
    if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_API_KEY_HERE":
        logger.warning("News API key not configured")
        return "News service is not configured. Please add your NewsAPI key in config.py"
    
    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': country,
            'apiKey': NEWS_API_KEY,
            'pageSize': min(count, 100)
        }
        
        if category:
            valid_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
            if category.lower() in valid_categories:
                params['category'] = category.lower()
        
        logger.info(f"Fetching news with params: {params}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"API Response status: {data.get('status')}")
        
        if data.get('status') != 'ok':
            error_msg = data.get('message', 'Unknown error')
            logger.error(f"NewsAPI error: {error_msg}")
            return f"News service returned error: {error_msg}"
        
        articles = data.get('articles', [])
        logger.info(f"Articles received: {len(articles)}")
        
        if not articles:
            if location:
                return search_news(f"{location} news", count=count)
            return "No news articles found at the moment."
        
        # Build response
        result = "Here are the latest news headlines: "
        for i, article in enumerate(articles[:min(3, len(articles))], 1):
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown source')
            
            # Truncate if too long
            if len(title) > 100:
                title = title[:97] + "..."
            
            result += f"{i}. {title} from {source}. "
        
        logger.info(f"News response built successfully")
        cache_response(cache_key, result, 1800)
        return result
        
    except requests.exceptions.Timeout:
        logger.error("News API timeout")
        return "News service timed out. Please try again."
    except requests.exceptions.ConnectionError:
        logger.error("News API connection error")
        return "Unable to connect to news service. Please check your internet."
    except Exception as e:
        logger.error(f"News error: {e}")
        return f"Error fetching news: {str(e)}"


def search_news(query, count=3):
    """Search for specific news topics"""
    if not NEWS_API_KEY or NEWS_API_KEY == "YOUR_API_KEY_HERE":
        return "News search service is not configured."
    
    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            'q': query,
            'apiKey': NEWS_API_KEY,
            'pageSize': min(count, 100),
            'sortBy': 'publishedAt',
            'language': 'en'
        }
        
        logger.info(f"Searching news for: {query}")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') != 'ok':
            error_msg = data.get('message', 'Unknown error')
            logger.error(f"NewsAPI search error: {error_msg}")
            return f"Search error: {error_msg}"
        
        articles = data.get('articles', [])
        
        if not articles:
            return f"No news found about '{query}'. Try other topics."
        
        result = f"News about {query}: "
        for i, article in enumerate(articles[:min(count, len(articles))], 1):
            title = article.get('title', 'No title')
            source = article.get('source', {}).get('name', 'Unknown')
            
            if len(title) > 80:
                title = title[:77] + "..."
            
            result += f"{i}. {title} ({source}). "
        
        logger.info(f"News search completed")
        return result
        
    except requests.exceptions.Timeout:
        logger.error("News search timeout")
        return f"Search for '{query}' timed out."
    except Exception as e:
        logger.error(f"News search error: {e}")
        return f"Error searching news: {str(e)}"


# ==================== WIKIPEDIA API ====================
# REMOVED: Wikipedia functionality removed - all queries now go to Gemini AI


# ==================== SYSTEM INFO ====================

def get_system_info():
    """Get system information"""
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_available = round(memory.available / (1024**3), 2)
        
        battery = psutil.sensors_battery()
        battery_info = ""
        if battery:
            battery_percent = int(battery.percent)
            plugged = "plugged in" if battery.power_plugged else "on battery"
            battery_info = f"Battery is at {battery_percent} percent and {plugged}. "
        
        result = (f"System status: CPU usage is at {cpu_percent} percent. "
                 f"Memory usage is at {memory_percent} percent with {memory_available} gigabytes available. "
                 f"{battery_info}")
        
        return result
        
    except Exception as e:
        logger.error(f"System info error: {e}")
        return "I couldn't fetch system information right now."


def get_disk_info():
    """Get disk usage information"""
    try:
        import psutil
        
        disk = psutil.disk_usage('/')
        total = round(disk.total / (1024**3), 2)
        used = round(disk.used / (1024**3), 2)
        free = round(disk.free / (1024**3), 2)
        percent = disk.percent
        
        result = (f"Disk usage: {used} gigabytes used out of {total} gigabytes total. "
                 f"{free} gigabytes free. That's {percent} percent used.")
        
        return result
        
    except Exception as e:
        logger.error(f"Disk info error: {e}")
        return "I couldn't fetch disk information."


# ==================== TIME & DATE ====================

def get_current_time():
    """Get current time"""
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    return f"The current time is {time_str}"


def get_current_date():
    """Get current date"""
    now = datetime.now()
    date_str = now.strftime("%A, %B %d, %Y")
    return f"Today is {date_str}"


# ==================== JOKES & ENTERTAINMENT ====================

def get_random_joke():
    """Get a random joke"""
    try:
        url = "https://official-joke-api.appspot.com/random_joke"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        
        setup = data.get('setup', '')
        punchline = data.get('punchline', '')
        
        return f"{setup} ... {punchline}"
        
    except Exception as e:
        logger.error(f"Joke API error: {e}")
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why did the scarecrow win an award? He was outstanding in his field!"
        ]
        import random
        return random.choice(jokes)


def get_random_fact():
    """Get a random interesting fact"""
    try:
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        
        fact = data.get('text', '')
        return f"Here's an interesting fact: {fact}"
        
    except Exception as e:
        logger.error(f"Fact API error: {e}")
        return "Did you know that honey never spoils?"


# ==================== MAIN API ROUTER ====================

def handle_api_request(intent, entities, query):
    """
    Main router for API requests based on intent
    Returns response string
    """
    try:
        if intent == 'weather':
            # Get default location from config if available
            try:
                from engine.config import DEFAULT_LOCATION
                default_location = DEFAULT_LOCATION.split(',')[0].strip() if DEFAULT_LOCATION else 'Bengaluru'
            except:
                default_location = 'Bengaluru'
            location = entities.get('location', default_location)
            logger.info(f"Weather request for location: {location}")
            return get_weather(location)
        
        elif intent == 'news':
            category = entities.get('category')
            location = entities.get('location')
            return get_news_headlines(category=category, location=location)
        
        elif intent == 'time_query':
            return get_current_time()
        
        elif intent == 'date_query':
            return get_current_date()
        
        elif intent == 'system_info':
            return get_system_info()
        
        elif intent == 'web_search':
            search_query = entities.get('search_query', query)
            # Wikipedia removed - return None to use Gemini AI instead
            return None
        
        elif intent == 'general_query':
            # Wikipedia removed - return None to use Gemini AI instead
            return None
        
        else:
            return None
            
    except Exception as e:
        logger.error(f"API request error: {e}")
        return None