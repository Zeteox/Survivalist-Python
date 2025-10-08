from events import get_random_event


class Day:
    def __init__(self):
        self.event = get_random_event()

    def get_event(self):
        return self.event