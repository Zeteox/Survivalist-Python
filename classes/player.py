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

    def is_alive(self) -> bool:
        if self.get_energy() == 0 or self.get_hunger() == 100 or self.get_thirst() == 100:
            self.set_alive(False)
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

    def show_stats(self) -> None:
        print(f"--- Player Stats ---\n"
              f"name: {self.get_name()}\n"
              f"Hunger: {self.get_hunger()}\n"
              f"Thirst: {self.get_thirst()}\n"
              f"Energy: {self.get_energy()}\n"
              f"--------------------\n")

    def fishing(self) -> None:
        if self.get_hunger() >= 10:
            self.set_hunger(self.get_hunger() - 10)
        else:
            self.set_hunger(0)
        if self.get_energy() >= 10:
            self.set_energy(self.get_energy() - 10)
        else:
            self.set_energy(0)
            self.set_alive(False)

    def find_water(self) -> None:
        if self.get_thirst() >= 10:
            self.set_thirst(self.get_thirst() - 10)
        else:
            self.set_thirst(0)
        if self.get_energy() >= 10:
            self.set_energy(self.get_energy() - 10)
        else:
            self.set_energy(0)
            self.set_alive(False)

    def sleeping(self) -> None:
        if self.get_hunger() <= 90:
            self.set_hunger(self.get_hunger() + 10)
        else:
            self.set_hunger(100)
            self.set_alive(False)
        if self.get_thirst() <= 90:
            self.set_thirst(self.get_thirst() + 10)
        else:
            self.set_thirst(100)
            self.set_alive(False)
        if self.get_energy() <= 90:
            self.set_energy(self.get_energy() + 10)
        else:
            self.set_energy(100)

    def do_action(self) -> None:
        if self.action_done:
            raise Exception("Action already done")
        else:
            print("What is your next action? (Fishing | Find water | Sleeping | Explore)")
            choice = input('Action: ').lower().strip()
            match choice:
                case "fishing":
                    self.fishing()
                case "find water":
                    self.find_water()
                case "sleeping":
                    self.sleeping()
                case "explore":
                    print('you have explore the forest')
                case _:
                    self.do_action()
            self.set_action_done(True)