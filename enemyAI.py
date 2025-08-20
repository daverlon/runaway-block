from game import GameState, ACTIONS

MAX_ITERATIONS = 5

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def enemy_ai_avoid(root: GameState):
    paths = search(root, [], 0)
    best = max(paths, key=lambda x: x['score'])
    print(f"Best path: {best['path']}, score: {best['score']}")
    return best['path'][0]

def search(node: GameState, path: list, depth: int) -> list:
    action_mask = node.get_entity_action_mask(node.enemy_id)

    if depth >= MAX_ITERATIONS or not action_mask:
        score = manhattan_distance(node.ents[node.player_id].x,
                                   node.ents[node.player_id].y,
                                   node.ents[node.enemy_id].x,
                                   node.ents[node.enemy_id].y)
        return [{'path': path, 'score': score}]

    all_paths = []
    for action in action_mask:
        new_node = node.copy()
        new_node = new_node.process_entity_action(new_node.enemy_id, action)
        results = search(new_node, path + [action], depth + 1)
        all_paths.extend(results)

    return all_paths