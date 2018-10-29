import numpy as np

CLASSIFICATION_PLAYER = 0
CLASSIFICATION_OBJECT = 1
CLASSIFICATION_BACKGROUND = 2

DIRECTION_LEFT = 3
DIRECTION_RIGHT = 2

def get_RGB_classification(rgb_array):
    global CLASSIFICATION_PLAYER, CLASSIFICATION_OBJECT, CLASSIFICATION_BACKGROUND
    rgb_sum = int(rgb_array[0]) + int(rgb_array[1]) + int(rgb_array[2])
    rgb_eq = int(rgb_array[0]) == int(rgb_array[1]) and int(rgb_array[1]) == int(rgb_array[2])
    return CLASSIFICATION_BACKGROUND if rgb_sum == 0 else (CLASSIFICATION_OBJECT if rgb_eq else CLASSIFICATION_PLAYER)


def get_entities_blueprints(observation):
    global CLASSIFICATION_PLAYER, CLASSIFICATION_OBJECT, CLASSIFICATION_BACKGROUND
    player_position = []
    obj_position = []
    #please excuse me for casting all of these fancy ndarrays to lists like a pleb
    for row_idx in range(len(observation)):
        for column_idx in range(len(observation[row_idx].tolist())):
            classification = get_RGB_classification(observation[row_idx][column_idx])
            if classification == CLASSIFICATION_PLAYER:
                player_position.append((row_idx, column_idx))
            if classification == CLASSIFICATION_OBJECT:
                obj_position.append((row_idx, column_idx))

    return (player_position, obj_position)


def get_player_indicators(blueprint):
    sum_X = 0
    lowest_X = 9999
    highest_X = 0
    highest_Y = 0

    for position in blueprint:
        sum_X += position[1]
        if position[1] > highest_X:
            highest_X = position[1]
        if position[1] < lowest_X:
            lowest_X = position[1]
        if position[0] > highest_Y:
            highest_Y = position[0]

    center_X = sum_X // len(blueprint)
    return (center_X, highest_Y, (highest_X - lowest_X) // 2)


def get_object_indicators(blueprint):
    sum_X = 0
    lowest_X = 9999
    highest_X = 0
    lowest_Y = 0

    for position in blueprint:
        sum_X += position[1]
        if position[1] > highest_X:
            highest_X = position[1]
        if position[1] < lowest_X:
            lowest_X = position[1]
        if position[0] < lowest_Y:
            lowest_Y = position[0]

    center_X = sum_X // len(blueprint)
    return (center_X, lowest_Y, (highest_X - lowest_X) // 2)


def is_it_worth_to_run(player_indicators, obj_indicators):
    steps_till_hit = (obj_indicators[1] - player_indicators[1]) / 2
    if player_indicators[0] < obj_indicators[0]:
        diff = (obj_indicators[0] - obj_indicators[1]) - (player_indicators[0] + player_indicators[2])
    else:
        diff = (player_indicators[0] - player_indicators[2]) - (obj_indicators[0] + obj_indicators[1])
    return diff +  steps_till_hit > 0


def where_to_run(player_indicators, obj_indicators):
    player_to_obj_rel = 0
    if player_indicators[0] < obj_indicators[0]:
        player_to_obj_rel = DIRECTION_LEFT
        diff = (obj_indicators[0] - obj_indicators[2]) - (player_indicators[0] + player_indicators[2])
    else:
        player_to_obj_rel = DIRECTION_RIGHT
        diff = (player_indicators[0] - player_indicators[2]) - (obj_indicators[0] + obj_indicators[1])
    return 1 if diff > 0 else player_to_obj_rel


def live_to_fight_another_day(player_center_X, width):
    center = width // 2 
    return 1 if player_center_X == center else (0 if player_center_X > center else 2)


class NotSoDumbAgend:
    def __init__(self, max_action: int):
        self.max_action = max_action

    def act(self, observation: np.ndarray):
        """
        :param observation: numpy array of shape (width, height, 3) *defined in config file
        :return: int between 0 and max_action
        """
        player_blueprint, obj_blueprint = get_entities_blueprints(observation)
        if len(obj_blueprint) == 0:
            return 1

        # just unpacking to save the reader from mental mapping variables
        player_center_X, player_highest_Y, player_width = get_player_indicators(player_blueprint)
        obj_center_X, obj_lowest_Y, obj_width = get_object_indicators(obj_blueprint)

        player_indicators = (player_center_X, player_highest_Y, player_width)
        obj_indicators = (obj_center_X, obj_lowest_Y, obj_width)

        if is_it_worth_to_run(player_indicators, obj_indicators):
            return where_to_run(player_indicators, obj_indicators)

        return live_to_fight_another_day(player_center_X, len(observation[0].tolist()))
