class Player:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.thirst = 0
        self.energy = 100
        self.action_done = False
        self.alive = True

    def get_name(self) -> str:
        return self.name

    def get_hunger(self) -> int:
        return self.hunger

    def get_thirst(self) -> int:
        return self.thirst

    def get_energy(self) -> int:
        return self.energy

    def get_action_done(self) -> bool:
        return self.action_done

    def get_alive(self) -> bool:
        return self.alive

    def set_name(self, name: str) -> None:
        self.name = name

    def set_hunger(self, hunger: int) -> None:
        self.hunger = hunger

    def set_thirst(self, thirst: int) -> None:
        self.thirst = thirst

    def set_energy(self, energy: int) -> None:
        self.energy = energy

    def set_action_done(self, action_done: bool) -> None:
        self.action_done = action_done

    def set_alive(self, alive: bool) -> None:
        self.alive = alive

    def get_stats(self):
        return {
            'name': self.name,
            'hunger': self.hunger,
            'thirst': self.thirst,
            'energy': self.energy
        }


