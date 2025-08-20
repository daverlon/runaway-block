
MAP_SIZE = 10

ACTIONS = ["move_up", "move_down", "move_left", "move_right"]

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GameState:
    def __init__(self):
        self.ents = []
        self.player_id = self.add_entity(0, 0)
        self.enemy_id = self.add_entity(5, 5)

    def add_entity(self, x, y) -> int:
        self.ents.append(Entity(x, y))
        return len(self.ents) - 1

    def get_entity_action_mask(self, ent_id) -> list:
        mask = []
        x, y = self.ents[ent_id].x, self.ents[ent_id].y
        if (x > 0): mask.append("move_left")
        if (x < MAP_SIZE - 1): mask.append("move_right")
        if (y > 0): mask.append("move_up")
        if (y < MAP_SIZE - 1): mask.append("move_down")
        return mask

    def process_entity_action(self, ent_id, action):
        if action == "move_up": self.ents[ent_id].y -= 1
        elif action == "move_down": self.ents[ent_id].y += 1
        elif action == "move_left": self.ents[ent_id].x -= 1
        elif action == "move_right": self.ents[ent_id].x += 1
        return self.copy()

    def copy(self):
        new_state = GameState()
        new_state.ents = [Entity(ent.x, ent.y) for ent in self.ents]
        return new_state