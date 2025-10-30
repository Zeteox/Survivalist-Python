import random
import time

from services.jsonServices import json_reader
from utils import miniGameUtils
from utils.displayUtils import clear_screen
from art import tprint

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
        tprint(f"--- Player  Stats ---\n"
              f"name:  {self.get_name()}\n"
              f"Hunger:  {100 - self.get_hunger()}\n"
              f"Thirst:  {100 - self.get_thirst()}\n"
              f"Energy:  {self.get_energy()}\n"
              f"----------------------\n", "tarty1")

    def find_water(self) -> None:
        """
        Player attempts to find water by completing a challenge.
        He must memorize and input a sequence of directions (N, S, E, W).
        If successful, thirst decreases; if not, thirst increases and energy decreases.
        :param self: Player instance
        :return: None
        """
        clear_screen()
        tprint("You  are  trying  to  find  water...\nYou'll need to memorize a sequence.\nGood  luck!\n", "tarty1")
        input("press enter when you are ready...")
        length = random.randint(1, 8)
        seq_expected = miniGameUtils.memory_sequence_challenge(length=length)
        tprint("Enter  the  sequence  of  directions (ex:  N  S  E  W  ou  NSEW)", "small")
        answer = "".join(input("Sequence : ").upper().strip())
        if answer == seq_expected:
            tprint("Congratulations!  You  found  water.", "small")
            self.set_thirst(self.get_thirst() - 30)
            self.set_energy(self.get_energy() - 5)
        else:
            tprint("You  got  lost  while  searching  for  water.\nYou  are  more  thirsty  and  tired.", "small")
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
        tprint("You have choose to go to sleep...\nAnd now your make a dream...\n-   -   -", "small")
        tprint(story["story"]+"\n-   -   -", "small")
        input("Press enter to continue...")

    def explore(self) -> None:
        """
        The player explores the environment, triggering a random event.
        :param self: Player instance
        :type self: Player
        :return: None
        """
        from classes.events import do_random_event
        clear_screen()
        tprint("You decided to explore the environment...", "small")
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
        tprint("When  the  fish  appears,  press  the  space  bar  while  it  is  visible.\n(If  you  aren't  on  Windows,  press  Enter  instead)", "small")
        tprint("Get  ready...","small")
        input("Press Enter to start...")

        wait_time = random.uniform(2.0, 5.0)
        time.sleep(wait_time)
        display_time = random.uniform(0.5, 1.5)

        # Display fish and start timing
        clear_screen()
        tprint("The  fish  has  appeared!  Press  Space  now!", "small")
        if fish and isinstance(fish, dict) and fish.get("design"):
            print(fish["design"])
        start_display = time.perf_counter()

        is_pressed_space = miniGameUtils.is_spacebar_pressed(display_time, start_display)

        # Display result and update stats
        if is_pressed_space:
            tprint(f"Congratulations!  You  caught  a  {fish["name"]}!", "small")
            self.set_hunger(self.get_hunger() - fish["hunger"])
            self.set_energy(self.get_energy() - fish["energy"])
        else:
            tprint("You  missed  the  fish. Better  luck  next  time!", "small")
            self.set_energy(self.get_energy() - fish["energy"])
        time.sleep(2)

    def do_action(self) -> None:
        """
        The player chooses and performs an action: fish, find water, sleep, or explore.
        :param self: Player instance
        :return: None
        """
        if self.action_done:
            raise Exception("Action already done")
        else:
            tprint("What is your next action?\n"
                   "1     : Fish                         |    2: Find water    |    3: Sleep\n"
                   "4: Explore    |    5: Cancel")
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
                case "5" | "cancel":
                    return None
                case _:
                    print("Invalid action")
                    return self.do_action()
            self.set_action_done(True)
            return None
