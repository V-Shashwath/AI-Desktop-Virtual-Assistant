"""
Significantly Improved NLP Module with Broader Scope
Handles all types of queries including system commands, general queries, etc.
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_conversation_context = {
    'last_intent': None,
    'last_entities': {},
    'last_query_time': None,
    'conversation_state': 'idle'
}

_lemmatizer = None
_stop_words = None


def initialize_nltk():
    """Download and initialize NLTK resources"""
    global _lemmatizer, _stop_words
    
    required_packages = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'omw-1.4']
    
    for package in required_packages:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            try:
                nltk.download(package, quiet=True)
                logger.info(f"Downloaded NLTK package: {package}")
            except Exception as e:
                logger.warning(f"Could not download {package}: {e}")
    
    _lemmatizer = WordNetLemmatizer()
    try:
        _stop_words = set(stopwords.words('english'))
    except:
        _stop_words = set()
    
    logger.info("NLTK initialized successfully")


def preprocess_text(text):
    """Clean and tokenize text"""
    global _lemmatizer, _stop_words
    
    if _lemmatizer is None:
        initialize_nltk()
    
    text = text.lower().strip()
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = word_tokenize(text)
    
    important_words = {'open', 'close', 'send', 'call', 'play', 'search', 'find', 
                       'what', 'who', 'where', 'when', 'how', 'volume', 'brightness',
                       'battery', 'screenshot', 'brightness', 'window', 'tab', 'news',
                       'weather', 'time', 'date', 'lock', 'shutdown', 'restart'}
    
    processed = []
    for token in tokens:
        if token not in _stop_words or token in important_words:
            lemma = _lemmatizer.lemmatize(token)
            processed.append(lemma)
    
    return processed


def extract_intent(query):
    """
    Extract user intent from query with VERY BROAD scope
    Includes system commands, APIs, apps, and general queries
    """
    query_lower = query.lower().strip()
    
    # EXPANDED INTENT RULES - Much broader scope
    intent_rules = {
        # === SYSTEM COMMANDS (HIGH PRIORITY) ===
        'volume_control': {
            'patterns': [
                r'\b(volume|sound)\s+(up|increase|loud)',
                r'\b(increase|raise)\s+(volume|sound)',
                r'\bouder\b',
                r'\bvolume\s+up\b'
            ],
            'keywords': ['volume', 'sound', 'up', 'increase', 'loud'],
            'priority': 15,
            'sub_type': 'volume_up'
        },
        'volume_down': {
            'patterns': [
                r'\b(volume|sound)\s+(down|decrease|low)',
                r'\b(decrease|lower)\s+(volume|sound)',
                r'\bquieter\b',
                r'\blower\s+volume\b'
            ],
            'keywords': ['volume', 'sound', 'down', 'decrease', 'quiet'],
            'priority': 15,
            'sub_type': 'volume_down'
        },
        'mute': {
            'patterns': [r'\bmute\b', r'\bsilence\b', r'\bmute\s+sound\b'],
            'keywords': ['mute', 'silence'],
            'priority': 15
        },
        'brightness_up': {
            'patterns': [
                r'\bbrightness\s+(up|increase)',
                r'\b(increase|raise)\s+brightness',
                r'\bbrighter\b',
                r'\bincrease\s+screen\b'
            ],
            'keywords': ['brightness', 'up', 'increase', 'brighter', 'screen'],
            'priority': 15,
            'sub_type': 'brightness_up'
        },
        'brightness_down': {
            'patterns': [
                r'\bbrightness\s+(down|decrease)',
                r'\b(decrease|lower)\s+brightness',
                r'\bdimmer\b',
                r'\b(dim|decrease)\s+screen\b'
            ],
            'keywords': ['brightness', 'down', 'decrease', 'dimmer', 'dim'],
            'priority': 15,
            'sub_type': 'brightness_down'
        },
        'battery_status': {
            'patterns': [
                r'\bbattery\b',
                r'\bbattery\s+(status|level|percentage)',
                r'\bhow\s+(much|much)\s+battery',
                r'\bbattery\s+info\b'
            ],
            'keywords': ['battery', 'status', 'level'],
            'priority': 14
        },
        'screenshot': {
            'patterns': [
                r'\b(take|capture)\s+(screenshot|screen)',
                r'\bscreenshot\b',
                r'\bprint\s+screen\b'
            ],
            'keywords': ['screenshot', 'capture', 'screen'],
            'priority': 14
        },
        'window_close': {
            'patterns': [
                r'\b(close|exit)\s+(window|this)',
                r'\bclose\s+this\b'
            ],
            'keywords': ['close', 'window'],
            'priority': 14
        },
        'window_minimize': {
            'patterns': [
                r'\bminimize\s+(window|this)',
                r'\bminimize\b'
            ],
            'keywords': ['minimize', 'minimise','window'],
            'priority': 14
        },
        'window_maximize': {
            'patterns': [
                r'\bmaximize\s+(window|this)',
                r'\bmaximize\b'
            ],
            'keywords': ['maximize', 'window'],
            'priority': 14
        },
        'lock_system': {
            'patterns': [
                r'\b(lock|lock)\s+(system|computer|pc)',
                r'\block\s+screen\b'
            ],
            'keywords': ['lock', 'system'],
            'priority': 14
        },
        'shutdown': {
            'patterns': [
                r'\bshutdown\b',
                r'\bshut\s+down\b',
                r'\bturn\s+off\b'
            ],
            'keywords': ['shutdown', 'off'],
            'priority': 14
        },
        'restart': {
            'patterns': [
                r'\brestart\b',
                r'\breboot\b'
            ],
            'keywords': ['restart', 'reboot'],
            'priority': 14
        },
        
        # === APPLICATION CONTROL ===
        'open_app': {
            'patterns': [
                r'\b(open|launch|start|run)\s+(\w+)',
                r'\bopen\s',
                r'\blaunch\s'
            ],
            'keywords': ['open', 'launch', 'start', 'run'],
            'priority': 12
        },
        
        # === YOUTUBE COMMANDS ===
        'youtube_play': {
            'patterns': [
                r'\b(play|watch)\s+(.+?)\s+(?:on\s+)?youtube',
                r'\bplay\b.+\byoutube\b'
            ],
            'keywords': ['play', 'youtube', 'watch'],
            'priority': 11
        },
        'youtube_search': {
            'patterns': [
                r'\bsearch\s+(.+?)\s+(?:on\s+)?youtube'
            ],
            'keywords': ['search', 'youtube'],
            'priority': 11
        },
        
        # === COMMUNICATION ===
        'send_message': {
            'patterns': [
                r'\b(send|text)\s+(?:a\s+)?message',
                r'\bsend\s+sms\b'
            ],
            'keywords': ['send', 'message', 'text', 'sms'],
            'priority': 12
        },
        'make_call': {
            'patterns': [
                r'\b(call|phone|dial)\s+',
                r'\bvoice\s+call\b'
            ],
            'keywords': ['call', 'phone', 'dial'],
            'priority': 12
        },
        'video_call': {
            'patterns': [
                r'\bvideo\s+call\b'
            ],
            'keywords': ['video', 'call'],
            'priority': 13
        },
        
        # === WEB SEARCH ===
        'web_search': {
            'patterns': [
                r'\b(search|find|google)\s+(?:for\s+)?(.+)',
                r'\blook\s+(up|for)\b'
            ],
            'keywords': ['search', 'find', 'google', 'look'],
            'priority': 10
        },
        
        # === EXTERNAL APIs ===
        'weather': {
            'patterns': [
                r'\b(weather|temperature|forecast|climate)\b',
                r'\bhow\s+(hot|cold)\b'
            ],
            'keywords': ['weather', 'temperature', 'forecast'],
            'priority': 11
        },
        'news': {
            'patterns': [
                r'\b(news|headlines|current\s+events)\b',
                r'\b(latest|today)\s+news\b'
            ],
            'keywords': ['news', 'headlines', 'events'],
            'priority': 11
        },
        'time_query': {
            'patterns': [
                r'\b(what.*time|tell.*time|current\s+time)\b',
                r'\bwhat\s+is\s+the\s+time\b'
            ],
            'keywords': ['time', 'clock'],
            'priority': 10
        },
        'date_query': {
            'patterns': [
                r'\b(what.*date|what.*day|today.*date)\b'
            ],
            'keywords': ['date', 'today', 'day'],
            'priority': 10
        },
        'system_info': {
            'patterns': [
                r'\b(system|cpu|memory|performance|disk)\b'
            ],
            'keywords': ['system', 'cpu', 'memory'],
            'priority': 10
        },
        
        # === GREETINGS ===
        'greeting': {
            'patterns': [
                r'^(hello|hi|hey|good\s+morning|good\s+evening)'
            ],
            'keywords': ['hello', 'hi', 'hey'],
            'priority': 5
        },
        'farewell': {
            'patterns': [
                r'\b(bye|goodbye|exit|quit|close|shutdown)\b'
            ],
            'keywords': ['bye', 'goodbye'],
            'priority': 6
        }
    }
    
    best_intent = 'general_query'
    best_score = 0
    matched_pattern = None
    sub_type = None
    
    # Check each intent
    for intent, rules in intent_rules.items():
        score = 0
        
        # Pattern matching
        for pattern in rules['patterns']:
            match = re.search(pattern, query_lower)
            if match:
                score += rules['priority'] * 2
                matched_pattern = pattern
                break
        
        # Keyword matching
        tokens = set(preprocess_text(query))
        keyword_matches = len(tokens.intersection(set(rules['keywords'])))
        score += keyword_matches * 1.5
        
        if score > best_score:
            best_score = score
            best_intent = intent
            sub_type = rules.get('sub_type')
    
    confidence = min(best_score / 20.0, 1.0)
    
    logger.info(f"Intent: {best_intent}, Confidence: {confidence:.2f}")
    return best_intent, confidence, matched_pattern, sub_type


def extract_entities(query, intent):
    """Extract entities based on intent"""
    entities = {}
    query_lower = query.lower()
    
    if intent == 'open_app':
        match = re.search(r'(?:open|launch|start|run)\s+(\w+)', query_lower)
        if match:
            entities['app_name'] = match.group(1)
    
    elif intent in ['youtube_play', 'youtube_search']:
        match = re.search(r'(?:play|search)\s+(.+?)\s+(?:on\s+)?youtube', query_lower)
        if not match:
            match = re.search(r'youtube\s+(.+)', query_lower)
        if match:
            search_term = match.group(1).strip()
            search_term = re.sub(r'\b(on|in|the|a|an)\b', '', search_term).strip()
            entities['search_term'] = search_term
    
    elif intent == 'send_message':
        match = re.search(r'(?:message|text|sms)\s+(?:to\s+)?(\w+)', query_lower)
        if match:
            entities['contact'] = match.group(1)
        entities['mode'] = 'whatsapp' if 'whatsapp' in query_lower else 'mobile'
    
    elif intent in ['make_call', 'video_call']:
        match = re.search(r'(?:call|phone|dial)\s+(?:to\s+)?(\w+)', query_lower)
        if match:
            entities['contact'] = match.group(1)
        entities['call_type'] = 'video' if 'video' in query_lower else 'voice'
        entities['mode'] = 'whatsapp' if 'whatsapp' in query_lower else 'mobile'
    
    elif intent == 'web_search':
        match = re.search(r'(?:search|find|google)\s+(?:for\s+)?(.+)', query_lower)
        if match:
            search_query = match.group(1).strip()
            search_query = re.sub(r'\s+(on|in)\s+(google|web)', '', search_query)
            entities['search_query'] = search_query
    
    elif intent == 'weather':
        match = re.search(r'(?:in|at|for)\s+(\w+)', query_lower)
        if match:
            entities['location'] = match.group(1)
        else:
            entities['location'] = 'Bengaluru'
    
    elif intent == 'news':
        categories = ['technology', 'sports', 'business', 'entertainment', 'health', 'india', 'local']
        for cat in categories:
            if cat in query_lower:
                entities['category'] = cat
                break
    
    return entities


def enhance_query_understanding(query, context=None):
    """Main NLP processing function"""
    global _conversation_context
    
    if _lemmatizer is None:
        initialize_nltk()
    
    tokens = preprocess_text(query)
    intent, confidence, pattern, sub_type = extract_intent(query)
    entities = extract_entities(query, intent)
    
    _conversation_context['last_intent'] = intent
    _conversation_context['last_entities'] = entities
    _conversation_context['last_query_time'] = datetime.now()
    
    result = {
        'query': query,
        'tokens': tokens,
        'intent': intent,
        'confidence': confidence,
        'entities': entities,
        'matched_pattern': pattern,
        'sub_type': sub_type,
        'timestamp': datetime.now().isoformat()
    }
    
    return result


def get_conversation_context():
    """Get current conversation context"""
    return _conversation_context.copy()


def reset_conversation_context():
    """Reset conversation context"""
    global _conversation_context
    _conversation_context = {
        'last_intent': None,
        'last_entities': {},
        'last_query_time': None,
        'conversation_state': 'idle'
    }
    logger.info("Conversation context reset")


def is_follow_up_query(query):
    """Check if query is a follow-up"""
    global _conversation_context
    
    if not _conversation_context['last_query_time']:
        return False
    
    time_diff = (datetime.now() - _conversation_context['last_query_time']).total_seconds()
    if time_diff > 300:
        return False
    
    follow_up_words = ['yes', 'no', 'okay', 'sure', 'mobile', 'whatsapp', 'that', 'this']
    query_words = query.lower().split()
    
    return any(word in follow_up_words for word in query_words)


def improve_query_with_context(query):
    """Improve query using context"""
    global _conversation_context
    
    if not is_follow_up_query(query):
        return query
    
    last_intent = _conversation_context.get('last_intent')
    last_entities = _conversation_context.get('last_entities', {})
    
    if query.lower() in ['yes', 'yeah', 'sure', 'okay', 'ok']:
        if last_intent == 'send_message' and 'contact' in last_entities:
            return f"send message to {last_entities['contact']}"
        elif last_intent == 'make_call' and 'contact' in last_entities:
            return f"call {last_entities['contact']}"
    
    if query.lower() in ['mobile', 'whatsapp']:
        if last_intent in ['send_message', 'make_call'] and 'contact' in last_entities:
            return f"{last_intent.replace('_', ' ')} to {last_entities['contact']} via {query}"
    
    return query


# Initialize on import
try:
    initialize_nltk()
except Exception as e:
    logger.error(f"Error initializing NLTK: {e}")