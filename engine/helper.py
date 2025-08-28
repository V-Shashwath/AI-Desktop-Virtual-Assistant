import os
import re
import time


def extract_yt_term(command):
    pattern = r'(play|search)\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return match.group(1).lower(), match.group(2)  # command type, search term
    return None, None