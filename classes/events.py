import os
import time
import random

from enum import Enum
from art import tprint
from classes.player import Player

class Event(Enum):
    RAIN = {"description": "It's  raining.", "impact": {"thirst": -10}}
    ENCOUNTER = {"description": "You  encounter  a  wild  animal.", "hunt": {"hunger": -15, "energy": -25}, "flee": {"thirst": 20,"energy": -20}}
    FIND = {"description": "You  find  a  hidden  stash  of  supplies.", "impact": {"hunger": -15, "thirst":-15}}

def get_random_event() -> Event:
    return random.choice(list(Event)).value

def do_random_event(player:Player, event=None) -> None:
        if event is None:
            event = get_random_event()
        tprint(f"{event["description"]}\n", "small")

        if ("impact" in event):
            tprint("Impact(s):", "small")
            for elem in event["impact"]:
                tprint("    -  "+elem+f"  ( {-event["impact"][elem]} )", "small")
            event_impact_effect(player, event["impact"])
        else:
            keys=list(event.keys())[1::]
            for option in keys:
                tprint(option+":", "small")
                for impact in event[option]:
                    invertOperator= 1 if impact == "energy" else -1
                    tprint("    -  "+impact+f"  ( {invertOperator * event[option][impact]} )", "small")

            choice = input("Choice: ").lower().strip()
            if choice in keys:
                event_impact_effect(player,event[choice])
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                os.system("cls" if os.name == "nt" else "clear")
                return do_random_event(player, event)
        input("Press enter to continue...")
        return

def event_impact_effect(player:Player,impacts:dict) -> None:
        for impact in impacts:
            match (impact):
                case "hunger":
                    player.set_hunger(player.get_hunger()+impacts[impact])
                case "thirst":
                    player.set_thirst(player.get_thirst()+impacts[impact])
                case "energy":
                    player.set_energy(player.get_energy()+impacts[impact])
                case _:
                    raise KeyError("Invalid key")