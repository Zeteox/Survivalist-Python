import time
from datetime import datetime

from art import tprint
from classes.player import Player
from services.jsonServices import json_reader, json_writer
from utils.displayUtils import clear_screen

SAVE_FILE_PATH = "./data/save/save.json"


def build_save_data(game, name: str) -> dict:
    """
    Build the save data dictionary.
    :param game: Instance of the game.
    :param name: Name of the save.
    :return: Dictionary containing the save data.
    """
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return {
        name.capitalize(): {
            "date": date,
            "difficulty": game.get_difficulty(),
            "current_days": game.get_current_days(),
            "victory_days": game.get_victory_days(),
            "random_event_done": game.get_random_event_done(),
            "player": {
                "name": game.player.get_name(),
                "hunger": game.player.get_hunger(),
                "thirst": game.player.get_thirst(),
                "energy": game.player.get_energy(),
                "action_done": game.player.get_action_done(),
                "alive": game.player.is_alive()
            }
        }
    }


def save_game(game) -> bool:
    """
    Saves the current game state to a JSON file. Prompts the user for confirmation and save name.
    If a save with the same name already exists, prompts the user for overwrite confirmation.
    :param game: Instance of the game.
    :return: True if the game was saved successfully, False otherwise.
    """
    print("Do you want to save your game? (Y/n):")
    choice = input().strip().lower()
    if choice not in {"y", "yes", ""}:
        print("You chose not to save the game.")
        input("Press enter to continue...")
        return True
    name = game.get_save_name()
    # Verify if the save name is set, otherwise ask for it
    if not name:
        print("What name would you like to give your save?")
        name = input("name your save: ").strip()
    # Check for empty save name
    if not name:
        print("Empty save name. Cancelling...")
        return False

    all_saves = json_reader(SAVE_FILE_PATH)
    game_data = build_save_data(game, name)

    # Check if a save with the same name already exists
    if isinstance(all_saves, dict):
        if name.capitalize() in all_saves:
            overwrite = input(f"A save with this name already exists. Do you want to overwrite it? (Y/n):\n")
            if overwrite.strip().lower() not in {"y", "yes", ""}:
                print("Save cancelled.")
                input("Press enter to continue...")
                return False
    else:
        all_saves = {}

    all_saves.update(game_data)

    print("Saving...")
    time.sleep(1)
    if json_writer(SAVE_FILE_PATH, all_saves):
        print(f"The {name.capitalize()} Game saved on {all_saves[name.capitalize()]["date"]}. !")
    else:
        print("An error occurred while saving the game. We apologize for the inconvenience.")
        return False
    return True


def load_params(game, selection_save: dict) -> None:
    game.chose_difficulty(selection_save.get("difficulty"))
    game.set_current_days(selection_save.get("current_days"))
    game.set_random_event_done(selection_save.get("random_event_done"))
    game.player = Player(selection_save.get("player").get("name"))
    game.player.set_hunger(selection_save.get("player").get("hunger"))
    game.player.set_thirst(selection_save.get("player").get("thirst"))
    game.player.set_energy(selection_save.get("player").get("energy"))
    game.player.set_action_done(selection_save.get("player").get("action_done"))
    game.player.set_alive(selection_save.get("player").get("alive"))


def display_saves(all_saves: list | dict | None) -> None:
    """
    Display the list of available saves.
    :param all_saves: Dictionary containing all saves.
    :return: None
    """
    print("Available saves:\n")
    for save_name in all_saves:
        save = all_saves.get(save_name)
        print(
            f"- {save_name} (Date: {save.get('date')}, Difficulty: {save.get('difficulty')}, Day: {save.get('current_days')}/{save.get('victory_days')})")


def load_game(game) -> bool:
    """
    Loads a saved game from the JSON file. Displays available saves and prompts the user to select one.
    Loads the selected save into the game instance. If the save does not exist, informs the user and returns False.
    :param game: Instance of the game.
    :return: True if the game was loaded successfully, False otherwise.
    """
    tprint("Loading game...", "tarty1")
    all_saves = json_reader(SAVE_FILE_PATH)
    if not all_saves:
        print("No saves found.")
        return False

    display_saves(all_saves)
    name = input("\nEnter the name of the save to load: ").strip()
    # Check if the save exists
    if name.capitalize() in all_saves:
        selection_save = all_saves.get(name.capitalize())
    else:
        clear_screen()
        tprint("Save not found.", "tarty1")
        time.sleep(1)
        return False

    clear_screen()
    tprint("Loading game...", "tarty1")
    load_params(game, selection_save)
    time.sleep(1)
    clear_screen()

    tprint(f"Game {name.capitalize()} loaded!", "tarty1")
    game.set_save_name(name.capitalize())
    time.sleep(2)
    return True


def delete_game(save_name: str) -> None:
    """
    Delete a saved game from the JSON file.
    :param save_name: Name of the save to delete.
    :return: None
    """
    all_saves = json_reader(SAVE_FILE_PATH)
    if not all_saves:
        return
    if save_name.capitalize() in all_saves:
        del all_saves[save_name.capitalize()]
        if json_writer(SAVE_FILE_PATH, all_saves):
            print(f"Save {save_name.capitalize()} deleted.")
        else:
            print("An error occurred while deleting the save. We apologize for the inconvenience.")
