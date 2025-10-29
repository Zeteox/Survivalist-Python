import random
import time

from classes.events import do_random_event
from services.jsonServices import json_reader
from utils import miniGameUtils
from utils.displayUtils import clear_screen


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

    def find_water(self) -> None:
        """
        Player attempts to find water by completing a challenge.
        He must memorize and input a sequence of directions (N, S, E, W).
        If successful, thirst decreases; if not, thirst increases and energy decreases.
        :param self: Player instance
        :return: None
        """
        clear_screen()
        print("You are trying to find water...\nGood luck!\n")
        length = random.randint(1, 8)
        seq_expected = miniGameUtils.memory_sequence_challenge(length=length)
        answer = "".join(input("Enter the sequence of directions (ex: N S E W ou NSEW) : ").upper().strip())
        if answer == seq_expected:
            print("Congratulations! You found water.")
            self.set_thirst(self.get_thirst() - 30)
            self.set_energy(self.get_energy() - 5)
        else:
            print("You got lost while searching for water. You are more thirsty and tired.")
            self.set_thirst(self.get_thirst() + 10)
            self.set_energy(self.get_energy() - 10)
        input("Press enter to continue...")

    def sleep(self) -> None:
        """
        The player sleeps. He recovers energy and loses hunger and thirst depending on his dream.
        :param self: Player instance
        :return: None
        """
        story = random.choice(json_reader("./data/sleep_story.json"))
        self.set_hunger(self.get_hunger() + story["hunger"])
        self.set_thirst(self.get_thirst() + story["thirst"])
        self.set_energy(self.get_energy() + story["energy"])
        clear_screen()
        print("You have choose to go to sleep...\nAnd now your make a dream...\n")
        print(story["story"])
        input("Press enter to continue...")

    def explore(self) -> None:
        """
        The player explores the environment, triggering a random event.
        :param self: Player instance
        :type self: Player
        :return: None
        """
        clear_screen()
        print("You decided to explore the environment...")
        do_random_event(self)

    def fish(self) -> None:
        """
        The player attempts to fish by completing a reflex challenge.
        He must press the space bar (or Enter) when a fish appears on the screen.
        If successful, hunger decreases; if not, energy decreases.
        :param self: Player instance
        :return: None
        """
        fish = miniGameUtils.get_fish()
        clear_screen()
        print("When the fish appears, press the space bar while it is visible. (If you aren't on Windows, press Enter instead)")
        input("Press Enter to start...")
        print("Get ready...")

        wait_time = random.uniform(2.0, 5.0)
        time.sleep(wait_time)
        display_time = random.uniform(0.5, 2.0)

        # Display fish and start timing
        clear_screen()
        print("The fish has appeared! Press Space now!")
        if fish and isinstance(fish, dict) and fish.get("design"):
            print(fish["design"])
        start_display = time.perf_counter()

        is_pressed_space = miniGameUtils.is_spacebar_pressed(display_time, start_display)

        # Display result and update stats
        clear_screen()
        if is_pressed_space:
            print(f"Congratulations! You caught a {fish["name"]}!")
            self.set_hunger(self.get_hunger() - fish["hunger"])
            self.set_energy(self.get_energy() - fish["energy"])
        else:
            print("You missed the fish. Better luck next time!")
            self.set_energy(self.get_energy() - fish["energy"])

    def do_action(self) -> None:
        """
        The player chooses and performs an action: fish, find water, sleep, or explore.
        :param self: Player instance
        :return: None
        """
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
