import os

from classes.player import Player


class Game:
    difficulty = 0
    victory_days = 0
    current_day = 0
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

    def get_current_day(self) -> int:
        return self.current_day

    def set_victory_days(self, days:int) -> None:
        if days < 1 :
            raise ValueError("Victory days cannot be negative or zero")
        self.victory_days = days

    def set_current_day(self, day:int) -> None:
        if day < 0:
            raise ValueError("Day cannot be negative")
        self.current_day = day

    def chose_difficulty(self, level:int) -> None:
        self.difficulty = level
        # Set victory days based on difficulty level
        self.set_victory_days(10 if level == 1 else 30 if level == 2 else 90 if level == 3 else -1)

    def next_day(self) -> None:
        self.current_day += 1

    def start(self):
        print(f"Starting the game: {self.title}")
        print("What is your name?")
        player_name = str(input("Enter your name: "))
        self.player = Player(player_name)
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Welcome to {self.get_title()}!")
        print("choose your difficulty level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
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
        print(f"Difficulty set to {self.get_difficulty()}")
        print(f"You need to survive for {self.get_victory_days()} days to win.")
        print(f"Good luck {self.player.get_name()}!")
        self.next_day()
        self.game_loop()

    def game_loop(self):
        while self.get_current_day() != self.get_victory_days()+1:
            os.system("cls" if os.name == "nt" else "clear")
            print(f" Day {self.get_current_day()}")
            # Here would be the game logic for each day
            self.next_day()
        print(f"Congratulations! You've survived {self.get_victory_days()} and won the game!")

Game("Crusoe").start()