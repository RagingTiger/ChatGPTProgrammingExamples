import numpy as np
import random

# Define board parameters
board_length = 40
houses_per_street = 3
board_streets = [
    "Mediterranean Avenue",
    "Baltic Avenue",
    "Oriental Avenue",
    "Vermont Avenue",
    "Connecticut Avenue",
    "St. Charles Place",
    "States Avenue",
    "Virginia Avenue",
    "St. James Place",
    "Tennessee Avenue",
    "New York Avenue",
    "Kentucky Avenue",
    "Indiana Avenue",
    "Illinois Avenue",
    "Atlantic Avenue",
    "Ventnor Avenue",
    "Marvin Gardens",
    "Pacific Avenue",
    "North Carolina Avenue",
    "Pennsylvania Avenue",
    "Park Place",
    "Boardwalk"
]

# Define game parameters
start_cash = 1500
player_count = 2

# Initialise the game
players = [{"player_name": "Player"+str(i),
            "player_position": 0,
            "player_cash": start_cash,
            "player_properties": []} for i in range(player_count)]

# Initialise Q-Table
Q = np.zeros([board_length, player_count, len(board_streets)])

# Define exploration rate
exploration_rate = 0.1

# Define learning rate
learning_rate = 0.8

# Define discount rate
discount_rate = 0.95

# Define reward parameters
property_value = 0.5
rent_value = 0.2

# Define actions
actions = ["buy house", "pass", "buy property"]

# Define maximum number of turns
max_turns = 100

# Define function to calculate reward
def calculate_reward(player):
    reward = 0
    for street in player["player_properties"]:
        if street["houses"] > 0:
            reward += rent_value * street["houses"]
        else:
            reward += property_value
    return reward

# Start the game
for turn in range(max_turns):
    # Roll the dice
    dice_roll = random.randint(2,12)
    # Iterate through the players
    for player in players:
        # Calculate the player's reward
        player["player_reward"] = calculate_reward(player)
        # Get the current state
        current_state = (player["player_position"], player["player_cash"])
        # Choose an action
        if np.random.rand() < exploration_rate:
            action = random.choice(actions)
        else:
            action = actions[np.argmax(Q[current_state])]
        # Execute the action
        if action == "buy house":
            if len(player["player_properties"]) > 0:
                street = random.choice(player["player_properties"])
                if street["houses"] < houses_per_street:
                    street["houses"] += 1
                    player["player_cash"] -= street["price"]
        elif action == "buy property":
            if player["player_position"] < board_length:
                street = board_streets[player["player_position"]]
                player["player_properties"].append({"name": street, "price": 50, "houses": 0})
                player["player_cash"] -= 50
        else:
            pass
        # Move the player
        player["player_position"] = (player["player_position"] + dice_roll) % board_length
        # Calculate the new reward
        new_reward = calculate_reward(player)
        # Get the new state
        new_state = (player["player_position"], player["player_cash"])
        # Update the Q-Table
        Q[current_state][actions.index(action)] = Q[current_state][actions.index(action)] + learning_rate * (new_reward + discount_rate * np.max(Q[new_state]) - Q[current_state][actions.index(action)])

# Print the Q-Table
print(Q)
