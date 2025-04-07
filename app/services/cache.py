import os
import json
import time
from datetime import datetime, timedelta

CACHE_DIR = os.path.join("app", "cache")
CACHE_EXPIRY = 3600  # Cache expiry in seconds (1 hour)

def get_cache_path(key):
    """Get the file path for a cache key"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    return os.path.join(CACHE_DIR, f"{key}.json")

def get_from_cache(key):
    """Get data from cache if it exists and is not expired"""
    cache_path = get_cache_path(key)
    
    if not os.path.exists(cache_path):
        return None
        
    # Check if cache is expired
    file_mod_time = os.path.getmtime(cache_path)
    if time.time() - file_mod_time > CACHE_EXPIRY:
        return None
        
    # Read from cache
    try:
        with open(cache_path, 'r') as f:
            return json.load(f)
    except:
        return None
        
def save_to_cache(key, data):
    """Save data to cache"""
    cache_path = get_cache_path(key)
    
    with open(cache_path, 'w') as f:
        json.dump(data, f) 
