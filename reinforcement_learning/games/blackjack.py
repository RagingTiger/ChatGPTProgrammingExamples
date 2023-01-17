import random

# Initialize Variables
dealer_score = 0
player_score = 0
player_cards = []
dealer_cards = []

# Initialize Constants
STAND = 0
HIT = 1

# Q-Table Initialization
Q = {}
for dealer_score in range(1,22):
    for player_score in range(4, 22):
        for player_card in range(2,11):
            for dealer_card in range(2,11):
                Q[((dealer_score, player_score, player_card, dealer_card), STAND)] = 0.0
                Q[((dealer_score, player_score, player_card, dealer_card), HIT)] = 0.0

# Hyperparameters
num_episodes = 1000
alpha = 0.1
gamma = 0.9

# Training
for e in range(num_episodes):

    # Initialize episode
    player_score = 0
    dealer_score = 0
    player_cards = []
    dealer_cards = []

    # Main loop of the game
    done = False
    while not done:

        # Player's turn
        if player_score < 21:
            # Get player's action
            action = random.choice([STAND, HIT])

            # Get reward for taking action
            if action == STAND:
                reward = 0
            elif action == HIT:
                player_cards.append(random.randint(2, 11))
                player_score = sum(player_cards)
                reward = 0
                if player_score > 21:
                    reward = -1
                    done = True

            # Update Q-Table
            Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), action)] += alpha * (reward + gamma * max(Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), STAND)], Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), HIT)]) - Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), action)])

        # Dealer's turn
        if dealer_score < 17:
            # Dealer must hit
            dealer_cards.append(random.randint(2, 11))
            dealer_score = sum(dealer_cards)
            if dealer_score > 21:
                reward = 1
                done = True
        else:
            # Dealer must stand
            if player_score > dealer_score:
                reward = 1
            elif player_score == dealer_score:
                reward = 0
            else:
                reward = -1
            done = True

# Use Q-Table to play blackjack
while True:
    # Deal Cards
    player_score = 0
    dealer_score = 0
    player_cards = []
    dealer_cards = []
    player_cards.append(random.randint(2, 11))
    dealer_cards.append(random.randint(2, 11))

    # Player's turn
    while player_score < 21:
        player_score = sum(player_cards)

        # Get action from Q-Table
        action = max(Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), STAND)], Q[((dealer_score, player_score, player_cards[-1], dealer_cards[0]), HIT)])

        if action == STAND:
            break
        elif action == HIT:
            player_cards.append(random.randint(2, 11))
            player_score = sum(player_cards)
            if player_score > 21:
                break

    # Dealer's turn
    while dealer_score < 17:
        dealer_cards.append(random.randint(2, 11))
        dealer_score = sum(dealer_cards)
        if dealer_score > 21:
            break

    # Determine Winner
    if player_score > 21:
        print("Player busted! You lose.")
    elif dealer_score > 21:
        print("Dealer busted! You win!")
    elif player_score > dealer_score:
        print("You win!"
    else:
        print("You lose!")

    play_again = input("Play again? (y/n): ")
    if play_again == "n":
        break

print("Thanks for playing!")
