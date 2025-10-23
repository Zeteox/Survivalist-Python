import time

from classes.player import Player
from services.jsonServices import json_reader, json_writer

SAVE_FILE_PATH = "../data/save/save.json"


def save_game(game) -> bool:
    name = game.get_save_name()
    if not name:
        print("What name would you like to give your save?")
        name = input("name your save: ").strip()

    if not name:
        print("Empty save name. Cancelling...")
        return False

    all_saves = json_reader(SAVE_FILE_PATH)
    date = time.strftime("%d/%m/%Y", time.localtime()) + " " + time.strftime("%H:%M:%S", time.localtime())
    game_data = {
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

    if isinstance(all_saves, dict):
        if name.capitalize() in all_saves:
            overwrite = input(f"A save with this name already exists. Do you want to overwrite it? (y/n):\n")
            if overwrite.strip().lower() not in {"y", "yes", ""}:
                print("Save cancelled.")
                return False
    else:
        all_saves = {}

    all_saves.update(game_data)

    print("Saving...")
    time.sleep(1)
    if json_writer(SAVE_FILE_PATH, all_saves):
        print(f"The {name.capitalize()} Game saved on {date} !")
    else:
        print("An error occurred while saving the game. We apologize for the inconvenience.")
        return False
    return True


def load_game(game) -> bool:
    all_saves = json_reader(SAVE_FILE_PATH)
    if not all_saves:
        print("No saves found.")
        return False

    print("Available saves:")
    for save_name in all_saves:
        save = all_saves.get(save_name)
        print(f"- {save_name} (Date: {save.get('date')}, Difficulty: {save.get('difficulty')}, Day: {save.get('current_days')}/{save.get('victory_days')})")
    print("Enter the name of the save you want to load:")
    name = input("Save name: ").strip()
    if name.capitalize() in all_saves:
        selection_save = all_saves.get(name.capitalize())
    else:
        print("Save not found.")
        return False

    print("Loading...")
    game.chose_difficulty(selection_save.get("difficulty"))
    game.set_current_days(selection_save.get("current_days"))
    game.set_random_event_done(selection_save.get("random_event_done"))
    game.player = Player(selection_save.get("player").get("name"))
    game.player.set_hunger(selection_save.get("player").get("hunger"))
    game.player.set_thirst(selection_save.get("player").get("thirst"))
    game.player.set_energy(selection_save.get("player").get("energy"))
    game.player.set_action_done(selection_save.get("player").get("action_done"))
    game.player.set_alive(selection_save.get("player").get("alive"))
    time.sleep(1)
    print(f"Game {name.capitalize()} loaded!")
    game.set_save_name(name.capitalize())
    return True

def delete_game(save_name: str) -> None:
    all_saves = json_reader(SAVE_FILE_PATH)
    if not all_saves:
        print("No saves found.")
        return
    if save_name.capitalize() in all_saves:
        del all_saves[save_name.capitalize()]
        if json_writer(SAVE_FILE_PATH, all_saves):
            print(f"Save {save_name.capitalize()} deleted.")
        else:
            print("An error occurred while deleting the save. We apologize for the inconvenience.")