import os


def clear_screen() -> None:
    """Function to clear the screen both onwindow as other OS.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
