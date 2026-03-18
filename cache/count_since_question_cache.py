import json
import diskcache as dc

cache = dc.Cache("./cache")

def update_count(chat_id, reset=False) -> None:
    if reset:
        cache[chat_id] = 0
    else:
        cache[chat_id] = cache.get(chat_id,0) + 1

def get_count(chat_id) -> int:
    return cache.get(chat_id,0)
