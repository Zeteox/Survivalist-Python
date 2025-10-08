from enum import Enum

class Event(Enum):
    RAIN = {"description": "It starts to rain.", "impact": {"thirst": -10}}
    ENCOUNTER = {"description": "You encounter a wild animal.", "hunt": {"hunger": -15, "energy": -25}, "flee": {"thirst": 20,"energy": -20}}
    FIND = {"description": "You find a hidden stash of supplies.", "impact": {"hunger": -10}}

def get_random_event():
    import random
    return random.choice(list(Event)).value