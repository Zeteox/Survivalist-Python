from enum import Enum

class Event(Enum):
    RAIN = "rain"
    ENCOUNTER = "encounter"
    FIND = "find"

def get_random_event():
    import random
    return random.choice(list(Event))