from random import choice

import pygame

from game import MAP_SIZE, GameState
from enemyAI import enemy_ai_avoid

def is_goal_state(game_state: GameState, player_id: int, enemy_id: int):
    return game_state.ents[player_id].x == game_state.ents[enemy_id].x and \
        game_state.ents[player_id].y == game_state.ents[enemy_id].y

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GAME!")

    game_state = GameState()
    player_id = game_state.player_id
    enemy_id = game_state.enemy_id

    entity_turn_id = player_id
    next_action = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    exit()

                if entity_turn_id == player_id:
                    player_action_mask = game_state.get_entity_action_mask(player_id)
                    # print(f"Player action mask: {player_action_mask}")
                    if event.key == pygame.K_UP: next_action = "move_up"
                    elif event.key == pygame.K_DOWN: next_action = "move_down"
                    elif event.key == pygame.K_LEFT: next_action = "move_left"
                    elif event.key == pygame.K_RIGHT: next_action = "move_right"
                    if next_action not in player_action_mask:
                        next_action = None
        # simulate

        if entity_turn_id == enemy_id:
            action = enemy_ai_avoid(game_state)
            game_state.process_entity_action(enemy_id, action)
            entity_turn_id = player_id

        if entity_turn_id == player_id:
            if next_action is not None:
                game_state.process_entity_action(player_id, next_action)
                entity_turn_id = enemy_id
                next_action = None
        

        if is_goal_state(game_state, player_id, enemy_id):
            print("Goal state reached!")
            pygame.quit()
            exit()
            
        # render
        pygame.display.get_surface().fill((0, 0, 0))

        for x in range(MAP_SIZE):
            for y in range(MAP_SIZE):
                rect = pygame.Rect(x * 80, y * 60, 80, 60)
                pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), rect, 1)

        for id, ent in enumerate(game_state.ents):
            rect = pygame.Rect(ent.x * 80, ent.y * 60, 80, 60)
            pygame.draw.rect(pygame.display.get_surface(), (int(id == enemy_id) * 255, int(id == player_id) * 255, 0), rect)

        pygame.display.flip()

