from enum import Enum
import os
import time

class Event(Enum):
    RAIN = {"description": "it's raining.", "impact": {"thirst": -10}}
    ENCOUNTER = {"description": "you encounter a wild animal.", "hunt": {"hunger": -15, "energy": -25}, "flee": {"thirst": 20,"energy": -20}}
    FIND = {"description": "you find a hidden stash of supplies.", "impact": {"hunger": -15, "thirst":-15}}

def get_random_event():
    import random
    return random.choice(list(Event)).value

def do_random_event(player, event=None):
        if event is None:
            event = get_random_event()
        print(f"{event["description"]}\n")

        player.show_stats()

        if ("impact" in event):
            print(f"Impacts: {event["impact"]}")
            event_impact_effect(player, event["impact"])
        else:
            print(f"Will you hunt it or flee?\n",
                  f"1: Hunt ({event['hunt']})\n"
                  f"2: Flee ({event['flee']})")
            choice = input("Choice: ")
            match (choice.lower().strip()):
                case "1":
                    event_impact_effect(player, event["hunt"])
                case "2":
                    event_impact_effect(player, event["flee"])
                case _:
                    print("Invalid choice. Please try again.")
                    time.sleep(1)
                    os.system("cls" if os.name == "nt" else "clear")
                    return do_random_event(player, event)
        input("Press enter to continue...")

def event_impact_effect(player,impacts):
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