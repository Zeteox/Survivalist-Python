import random
import time

from services.jsonServices import json_reader
from utils.displayUtils import clear_screen

# On Windows, msvcrt allows you to read a key without waiting for Enter.
try:
    import msvcrt
except Exception:
    msvcrt = None


def memory_sequence_challenge(length: int = 4) -> str:
    """Challenge where the player must memorize and input a sequence of directions.
    :param length: Length of the sequence to memorize.
    :type length: int
    :return: The generated (NSEW) sequence as a string.
    """
    options = ["N", "S", "E", "W"]
    seq = [random.choice(options) for _ in range(length)]
    display = " ".join(seq)
    print("Memorize this sequence:")
    print(display)
    time.sleep(1)
    clear_screen()
    return "".join(seq)


def get_fish() -> dict | None:
    """Return a random fish from the fishes.json file.
    :return: A dictionary representing a fish or None if an error occurs.
    """
    try:
        data = json_reader("./data/fishes.json")
        if not data:
            return None
        random_key = random.choice(list(data.keys()))
        return data[random_key]
    except Exception as e:
        return None


def is_spacebar_pressed(display_time: float, start_display: float) -> bool:
    """Detect if the spacebar is pressed within the display time.
    On Windows, uses msvcrt to detect spacebar press.
    :param display_time: Time in seconds the fish is displayed.
    :param start_display: Time when the fish was displayed.
    :return: True if spacebar was pressed in time, False otherwise.
    """
    if msvcrt:
        # On Windows, we use msvcrt to detect spacebar press.
        while msvcrt.kbhit():
            try:
                msvcrt.getch()
            except Exception:
                return False

        while True:
            now = time.perf_counter()
            reaction_time = now - start_display
            if reaction_time >= display_time:
                return False
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b' ':
                    return True
    else:
        # On non-Windows systems, we simulate spacebar press with Enter key.
        try:
            space = input()
            now = time.perf_counter()
            reaction_time = now - start_display
            if ' ' in space and reaction_time <= display_time:
                return True
        except Exception:
            return False
    return False
