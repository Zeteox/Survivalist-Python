from enum import Enum
import os

class Event(Enum):
    RAIN = {"description": "it's raining.", "impact": {"thirst": -10}}
    ENCOUNTER = {"description": "you encounter a wild animal.", "hunt": {"hunger": -15, "energy": -25}, "flee": {"thirst": 20,"energy": -20}}
    FIND = {"description": "you find a hidden stash of supplies.", "impact": {"hunger": -15, "thirst":-15}}

def get_random_event():
    import random
    return random.choice(list(Event)).value

def cli_days_event(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Day {self.get_current_days()}",
                f"A new morning rise on this cursed island and....\n",
                f"{self.get_random_event()["description"]}")
        if ("impact" in self.get_random_event()):
            print(f"Impacts: {self.get_random_event()["impact"]}")
            self.days_impact_effect(self.get_random_event()["impact"])
        else:
            print(f"Will you hunt it or flee? (H/F)")
            choice = input("Choice: ")
            match (choice.upper().strip()):
                case "H":
                    self.days_impact_effect(self.get_random_event()["hunt"])
                case "F":
                    self.days_impact_effect(self.get_random_event()["flee"])
                case _:
                    print("Invalid choice. Plese try again")
                    time.sleep(1)
                    self.cli_days_event()
                    return
        input("Press enter to continue...")