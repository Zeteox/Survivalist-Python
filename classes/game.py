import os
import time

from player import Player
from day import Day


class Game:
    difficulty = 0
    victory_days = 0
    current_days = 0
    player= None

    def __init__(self, title:str):
        self.title = title
        self.days_counter = 0

    def get_title(self) -> str:
        return self.title

    def get_difficulty(self) -> int:
        return self.difficulty

    def get_victory_days(self) -> int:
        return self.victory_days

    def get_current_days(self) -> int:
        return self.current_days

    def set_victory_days(self, days:int) -> None:
        if days < 1 :
            raise ValueError("Victory days cannot be negative or zero")
        self.victory_days = days

    def set_current_days(self, day:int) -> None:
        if day < 0:
            raise ValueError("Day cannot be negative")
        self.current_days = day

    def chose_difficulty(self, level:int) -> None:
        self.difficulty = level
        # Set victory days based on difficulty level
        self.set_victory_days(10 if level == 1 else 30 if level == 2 else 90)

    def next_day(self) -> None:
        self.current_days += 1

    def start_cli(self):
        print(f"Starting the game: {self.title}...")
        time.sleep(1.5)
        os.system("cls" if os.name == "nt" else "clear")
        print("What is your name?")
        player_name = str(input("Enter your name: "))
        self.player = Player(player_name)
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Welcome to {self.get_title()}!\n"
              f"choose your difficulty level:\n"
              f"1. Easy (10 days) \n"
              f"2. Medium (30 days) \n"
              f"3. Hard (90 days)")
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
        print(f"Difficulty set to {self.get_difficulty()}"
              f"You need to survive for {self.get_victory_days()} days to win."
              f"Good luck {self.player.get_name()}!")
        self.next_day()
        self.cli_game_loop()

    def show_menu(self):
        print("1. Start New Game")
        print("2. Load Game")
        print("3. Exit")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                self.start_cli()
            case "2":
                print("Load Game feature is not implemented yet.")
            case "3":
                print("Exiting the game. Goodbye!")
                exit()
    
    def show_game_menu(self):
        os.system("cls" if os.name == "nt" else "clear")
        print(f" Day {self.get_current_days()}")
        current_day = Day()
        print(f"\n{current_day.get_event()['description']}\n")
       
        stats = self.player.get_stats()
        print(f"--- Player Stats ---\n"
                f"name: {stats['name']}\n"
                f"Hunger: {stats['hunger']}\n"
                f"Thirst: {stats['thirst']}\n"
                f"Energy: {stats['energy']}\n"
                f"--------------------\n")
        print("1. Perform Action")
        print("2. End Day")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                try:
                    self.player.do_action()
                    time.sleep(1)
                    self.show_game_menu()
                except Exception as e:
                    print(f"Action already done")
                    time.sleep(1)
                    self.show_game_menu()
            case "2":
                self.next_day()
                self.player.set_action_done(False)
            case _:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                self.show_game_menu()

    def cli_game_loop(self):
        while self.get_current_days() != self.get_victory_days()+1:

            self.show_game_menu()

            if not self.player.is_alive():
                print("You have died. Game Over.")
                return
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Congratulations! You've survived {self.get_victory_days()} days and won the game!")

Game("Crusoe").show_menu()