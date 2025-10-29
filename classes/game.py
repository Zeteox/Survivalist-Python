import os
import random
import time

from art import tprint
from classes.events import do_random_event
from classes.action import do_action
from classes.player import Player
from services.saveServices import save_game, load_game, delete_game


class Game:
    title = "Crusoe"
    difficulty = 0
    victory_days = 0
    current_days = 0
    player = None
    random_event_done = False
    save_name = ""

    def __init__(self):
        self.days_counter = 0

    def get_title(self) -> str:
        return self.title

    def get_difficulty(self) -> int:
        return self.difficulty

    def get_victory_days(self) -> int:
        return self.victory_days

    def get_current_days(self) -> int:
        return self.current_days

    def get_random_event_done(self) -> bool:
        return self.random_event_done

    def get_save_name(self) -> str:
        return self.save_name

    def set_victory_days(self, days: int) -> None:
        if days < 1:
            raise ValueError("Victory days cannot be negative or zero")
        self.victory_days = days

    def set_current_days(self, day: int) -> None:
        if day < 0:
            raise ValueError("Day cannot be negative")
        self.current_days = day

    def set_random_event_done(self, done: bool) -> None:
        self.random_event_done = done

    def set_save_name(self, name: str) -> None:
        self.save_name = name

    def invert_random_event_done(self) -> None:
        if self.random_event_done:
            self.random_event_done = False
        else:
            self.random_event_done = True

    def chose_difficulty(self, level: int) -> None:
        self.difficulty = level
        # Set victory days based on difficulty level
        self.set_victory_days(10 if level == 1 else 30 if level == 2 else 90)

    def next_day(self) -> None:
        self.current_days += 1
        self.player.set_thirst(self.player.get_thirst() + 10)
        self.player.set_hunger(self.player.get_hunger() + 10)

    def restart(self) -> None:
        if input("restart ? (y/N): ").upper() in ["Y", "YES"]:
            return self.game_creator_cli()
        return self.exit_game_screen()

    def is_game_over(self) -> None:
        if not self.player.is_alive():
            self.clear_screen()
            tprint(f"Day  {self.get_current_days()}", "tarty1")
            self.player.show_stats()
            tprint("You  have  died.\nGame  Over.", "tarty1")
            delete_game(self.save_name)
            return self.restart()

    def clear_screen(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def load_game_screen(self) -> None:
        self.clear_screen()
        if not load_game(self):
            self.clear_screen()
            tprint("Returning to main menu...", "tarty1")
            time.sleep(1)
            return self.start()
        return self.cli_game_loop()

    def exit_game_screen(self) -> None:
        self.clear_screen()
        tprint("Exiting the game. Goodbye!", "tarty1")
        time.sleep(2)
        self.clear_screen()
        exit()

    def start(self) -> None:
        self.clear_screen()
        tprint(f"---  Welcome  to  {self.get_title()}  ---", "tarty1")
        tprint("1.  Start  New  Game","tarty1")
        tprint("2.  Load  Game","tarty1")
        tprint("3.  Exit","tarty1")
        match input("Enter your choice: "):
            case "1":
                return self.game_creator_cli()
            case "2":
                return self.load_game_screen()
            case "3":
                return self.exit_game_screen()
            case _:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                return self.start()

    def game_creator_cli(self) -> None:
        self.clear_screen()
        tprint(f"Starting  the  game...", "tarty1")
        time.sleep(0.5)
        self.clear_screen()
        tprint("Choose  your  name", "tarty1")
        self.player = Player(str(input("Enter your name: ")))
        self.clear_screen()
        tprint(f"Choose  your  difficulty:\n"
              f"1.  Easy  -  10 days\n"
              f"2.  Medium  -  30 days\n"
              f"3.  Hard  -  90 days", "tarty1")
        while True:
            try:
                level = int(input("Enter difficulty level (1-3): "))
                if level in [1, 2, 3]:
                    self.chose_difficulty(level)
                    break
                else:
                    print("Invalid choice. Please choose a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        tprint(f"Difficulty set to {self.get_difficulty()}.\n"
              f"You need to survive for {self.get_victory_days()} days to win.\n"
              f"Good luck player {self.player.get_name()}!", "small")
        time.sleep(3)
        self.current_days = 1
        self.cli_game_loop()

    def show_game_menu(self) -> None:
        self.clear_screen()
        tprint(f"Day  {self.get_current_days()}\n", "tarty1")
        self.player.show_stats()
        tprint(f"1. Perform  Action\n"
               f"2. End  Day\n"
               f"3. Exit  Game", "tarty1")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                try:
                    do_action(self, self.player)
                    return self.is_game_over()
                except Exception as e:
                    tprint(f"Action already done","tarty1")
                    time.sleep(1)
                return self.show_game_menu()
            case "2":
                self.is_game_over()
                self.player.set_action_done(False)
                self.invert_random_event_done()
                return self.next_day()
            case "3":
                if save_game(self):
                    time.sleep(1)
                    return self.exit_game_screen()
                else:
                    return self.show_game_menu()
            case _:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                return self.show_game_menu()

    def cli_game_loop(self) -> None:
        while self.get_current_days() != self.get_victory_days() + 1:
            self.is_game_over()
            self.clear_screen()
            if not self.random_event_done and random.randint(1,3) == 1 :
                tprint(f"Day {self.get_current_days()}\n", "tarty1")
                self.player.show_stats()
                tprint("A  new  morning  rise  on  this  cursed  island.", "small",)
                do_random_event(self.player)
                self.invert_random_event_done()
            else:
                self.random_event_done = True
            self.is_game_over()
            self.show_game_menu()
        self.clear_screen()
        delete_game(self.save_name)
        tprint(f"Congratulations!\nYou've survived {self.get_victory_days()} days!\nYou won the game!", "tarty1")
        self.restart()