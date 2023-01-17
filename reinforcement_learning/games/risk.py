#importing necessary libraries
import numpy as np
import random
from collections import deque

#Defining the Risk game environment
class RiskEnv:

    #Initializing the board with given parameters
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = np.zeros((board_size, board_size))
        self.player_position = (0,0)

    #Function to reset the environment
    def reset(self):
        self.board = np.zeros((self.board_size, self.board_size))
        self.player_position = (0,0)
        return self.board, self.player_position

    #Function to take an action
    def step(self, action):
        #Get the current position of the player
        row, col = self.player_position

        #Move one step in the specified direction
        if action == 0: # Left
            col = max(col - 1, 0)
        elif action == 1: # Right
            col = min(col + 1, self.board_size - 1)
        elif action == 2: # Up
            row = max(row - 1, 0)
        else: # Down
            row = min(row + 1, self.board_size - 1)

        #Update the position of the player
        self.player_position = (row, col)

        #Get the reward for taking the action
        reward = self.board[row, col]

        #Update the board
        self.board[row, col] = 0

        #Return the board, position and reward
        return self.board, self.player_position, reward

#Defining the Deep Q-learning agent
class DQNAgent:

    #Initializing the agent
    def __init__(self, env):
        self.env = env
        self.state_size = env.board_size
        self.action_size = 4
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    #Building a neural network
    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    #Function to remember experiences
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    #Function to act
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    #Function to replay experiences
    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma *
                          np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    #Function to load the pre-trained model
    def load(self, name):
        self.model.load_weights(name)

    #Function to save the pre-trained model
    def save(self, name):
        self.model.save_weights(name)
