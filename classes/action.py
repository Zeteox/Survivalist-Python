import os
import random
import time

from classes.events import do_random_event
from classes.player import Player
from services.jsonServices import json_reader


def fish(player: Player) -> None:
    player.set_hunger(player.get_hunger() - 10)
    player.set_energy(player.get_energy() - 10)
    player.is_alive()


def memory_sequence_challenge(length: int = 4) -> str:
    options = ["N", "S", "E", "W"]
    seq = [random.choice(options) for _ in range(length)]
    display = " ".join(seq)
    os.system("cls" if os.name == "nt" else "clear")
    print("Memorize this sequence:")
    print(display)
    time.sleep(1)
    os.system("cls" if os.name == "nt" else "clear")
    return "".join(seq)


def find_water(player: Player) -> None:
    length = random.randint(1, 8)
    seq_expected = memory_sequence_challenge(length=length)
    answer = "".join(input("Enter the sequence of directions (ex: N S E W ou NSEW) : ").upper().strip())
    if answer == seq_expected:
        print("Congratulations! You found water.")
        player.set_thirst(player.get_thirst() - 30)
        player.set_energy(player.get_energy() - 5)
    else:
        print("You got lost while searching for water. You are more thirsty and tired.")
        player.set_thirst(player.get_thirst() + 10)
        player.set_energy(player.get_energy() - 10)
    input("Press enter to continue...")
    player.is_alive()


def sleep(game, player: Player) -> None:
    story = random.choice(json_reader("./data/sleep_story.json"))
    player.set_hunger(player.get_hunger() + story["hunger"])
    player.set_thirst(player.get_thirst() + story["thirst"])
    player.set_energy(player.get_energy() + story["energy"])
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Day {game.get_current_days()}\n")
    game.player.show_stats()
    print(story["story"])
    input("Press enter to continue...")
    player.is_alive()


def explore(player: Player) -> None:
    do_random_event(player)
    player.name = "Explorer"
    player.is_alive()


def do_action(game, player: Player) -> None:
    if player.action_done:
        raise Exception("Action already done")
    else:
        print("What is your next action? (1: Fish | 2: Find water | 3: Sleep | 4: Explore)")
        choice = input('Action: ').lower().strip()
        match choice:
            case "1" | "fish":
                fish(player)
            case "2" | "find water":
                find_water(player)
            case "3" | "sleep":
                sleep(game, player)
            case "4" | "explore":
                explore(player)
            case _:
                print("Invalid action")
                return do_action(game, player)
        player.set_action_done(True)
        return None
