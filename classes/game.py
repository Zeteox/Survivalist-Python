import time

from art import tprint
from classes.events import do_random_event
from classes.player import Player
from services.saveServices import save_game, load_game, delete_game
from utils.displayUtils import clear_screen


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

    def is_game_over(self) -> None:
        if not self.player.is_alive():
            print(f"You have died on the {self.get_current_days()} day. Game Over.")
            delete_game(self.save_name)
            return

    def load_game_screen(self) -> None:
        clear_screen()
        if not load_game(self):
            clear_screen()
            tprint("Returning to main menu...", "tarty1")
            time.sleep(1)
            return self.start()
        return self.cli_game_loop()

    def exit_game_screen(self) -> None:
        clear_screen()
        tprint("Exiting the game. Goodbye!", "tarty1")
        time.sleep(2)
        clear_screen()
        exit()

    def start(self):
        clear_screen()
        tprint(f"--- Welcome to {self.get_title()} ---", "tarty1")
        tprint("1. Start New Game","tarty1")
        tprint("2. Load Game","tarty1")
        tprint("3. Exit","tarty1")
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

    def game_creator_cli(self):
        clear_screen()
        print(f"Starting the game...")
        time.sleep(0.5)
        clear_screen()
        print("What is your name?")
        player_name = str(input("Enter your name: "))
        self.player = Player(player_name)
        clear_screen()
        print(f"Choose your difficulty level:\n"
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
        self.current_days = 1
        self.cli_game_loop()

    def show_game_menu(self):
        clear_screen()
        print(f"Day {self.get_current_days()}\n")
        self.player.show_stats()
        print("1. Perform Action")
        print("2. End Day")
        print("3. Exit Game")
        choice = input("Enter your choice: ")
        match choice:
            case "1":
                try:
                    self.player.do_action()
                    time.sleep(1)
                    self.is_game_over()
                    self.show_game_menu()
                except Exception as e:
                    print(f"Action already done")
                    time.sleep(1)
                    self.show_game_menu()
            case "2":
                self.next_day()
                self.player.set_action_done(False)
                self.invert_random_event_done()
                return None
            case "3":
                if save_game(self):
                    print("Exiting the game. Goodbye!")
                    exit()
                else:
                    time.sleep(1)
                    return self.show_game_menu()
            case _:
                print("Invalid choice. Please try again.")
                time.sleep(1)
                return self.show_game_menu()

    def cli_game_loop(self):
        while self.get_current_days() != self.get_victory_days() + 1:
            clear_screen()
            print(f"Day {self.get_current_days()}",
                  f"A new morning rise on this cursed island and...")
            if not self.random_event_done:
                do_random_event(self.player)
                self.invert_random_event_done()

            self.is_game_over()

            self.show_game_menu()

        clear_screen()
        delete_game(self.save_name)
        print(f"Congratulations! You've survived {self.get_victory_days()} days and won the game!")