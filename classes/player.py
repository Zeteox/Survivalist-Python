import random

from classes.events import do_random_event
from services.jsonServices import json_reader


class Player:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.thirst = 0
        self.energy = 100
        self.action_done = False
        self.alive = True

    def get_name(self) -> str:
        return self.name

    def get_hunger(self) -> int:
        return self.hunger

    def get_thirst(self) -> int:
        return self.thirst

    def get_energy(self) -> int:
        return self.energy

    def get_action_done(self) -> bool:
        return self.action_done

    def is_alive(self) -> bool:
        if self.get_energy() == 0 or self.get_hunger() == 100 or self.get_thirst() == 100:
            self.set_alive(False)
        return self.alive

    def set_name(self, name: str) -> None:
        self.name = name

    def set_hunger(self, hunger: int) -> None:
        match hunger:
            case h if h < 0:
                hunger = 0
            case h if h > 100:
                hunger = 100
        self.hunger = hunger

    def set_thirst(self, thirst: int) -> None:
        match thirst:
            case t if t < 0:
                thirst = 0
            case t if t > 100:
                thirst = 100
        self.thirst = thirst

    def set_energy(self, energy: int) -> None:
        match energy:
            case e if e < 0:
                energy = 0
            case e if e > 100:
                energy = 100
        self.energy = energy

    def set_action_done(self, action_done: bool) -> None:
        self.action_done = action_done

    def set_alive(self, alive: bool) -> None:
        self.alive = alive

    def show_stats(self) -> None:
        print(f"--- Player Stats ---\n"
              f"name: {self.get_name()}\n"
              f"Hunger: {self.get_hunger()}\n"
              f"Thirst: {self.get_thirst()}\n"
              f"Energy: {self.get_energy()}\n"
              f"--------------------\n")

    def fish(self) -> None:
        self.set_hunger(self.get_hunger() - 10)
        self.is_alive()

    def find_water(self) -> None:
        self.set_thirst(self.get_thirst() - 10)
        self.set_energy(self.get_energy() - 10)
        self.is_alive()

    def sleep(self) -> None:
        story = random.choice(json_reader("../data/sleep_story.json"))
        print(story["story"])
        input("Press enter to continue...")
        self.set_hunger(self.get_hunger() + story["hunger"])
        self.set_thirst(self.get_thirst() + story["thirst"])
        self.set_energy(self.get_energy() + story["energy"])
        self.is_alive()

    def explore(self) -> None:
        do_random_event(self)
        self.is_alive()

    def do_action(self) -> None:
        if self.action_done:
            raise Exception("Action already done")
        else:
            print("What is your next action? (1: Fish | 2: Find water | 3: Sleep | 4: Explore)")
            choice = input('Action: ').lower().strip()
            match choice:
                case "1" | "fish":
                    self.fish()
                case "2" | "find water":
                    self.find_water()
                case "3" | "sleep":
                    self.sleep()
                case "4" | "explore":
                    self.explore()
                case _:
                    print("Invalid action")
                    return self.do_action()
            self.set_action_done(True)
            return None
