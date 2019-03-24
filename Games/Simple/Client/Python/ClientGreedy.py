def get_action(world):
    if world.goal_position.i > world.self_position.i:
        action = 'd'
    elif world.goal_position.i < world.self_position.i:
        action = 'u'
    elif world.goal_position.j > world.self_position.j:
        action = 'r'
    elif world.goal_position.j < world.self_position.j:
        action = 'l'
    return action