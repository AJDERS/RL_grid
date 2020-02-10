import numpy as np
from tqdm import tqdm
BOARD_ROWS = 3
BOARD_COLS = 4
HOLES = [(1,1)]
WIN_STATE = (0,3)
LOSE_STATE = (1,3)
START = (2,0)
DETERMINISTIC = True

class State:
    def __init__(self, state=START):
        assert LOSE_STATE != START, "Lose state equals start state."
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.board[1,1] = -1
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def defineHoles(self, holes):
        board = np.zeros([BOARD_ROWS, BOARD_COLS])
        for hole in holes:
           board[hole[0],hole[1]] = -1
        return board

    def giveReward(self):
        if self.state == WIN_STATE:
            return 1
        elif self.state == LOSE_STATE:
            return -1
        else:
            return -0.1

    def nextPosition(self, action):
        if self.determine:
            if action == "up":
                nextState = (self.state[0] - 1, self.state[1])
            elif action == "down":
                nextState = (self.state[0] + 1, self.state[1])
            elif action == "left":
                nextState = (self.state[0], self.state[1] - 1)
            else:
                nextState = (self.state[0], self.state[1] + 1)

            if (nextState[0] >= 0) and (nextState[0] <= BOARD_ROWS-1):
                if (nextState[1] >= 0) and (nextState[1] <= BOARD_COLS-1):
                    if nextState != (1,1):
                        return nextState
            return self.state	               

    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state == LOSE_STATE):
            self.isEnd = True
        
class Agent:
    
    def __init__(self):
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.lr = 0.2
        self.exp_rate = 0.3
        self.state_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.state_values[(i,j)] = 0

    def play(self, rounds=10):
        i = 0
        pbar = tqdm(total = rounds)
        while i < rounds:
            if self.State.isEnd:
                reward = self.State.giveReward()
                self.state_values[self.State.state] = reward
                for state in reversed(self.states):
                    reward = self.state_values[state] + self.lr * (reward - self.state_values[state])
                    self.state_values[state] = round(reward, 3)
                if i == rounds-1:
                    self.last_game = self.states
                self.reset()
                i += 1
                pbar.update(1)
            else:
                action = self.chooseAction()
                self.states.append(self.State.nextPosition(action))
                self.State = self.takeAction(action)
                self.State.isEndFunc()
        pbar.close()
        return "Last game,{}, {}, {}".format(reward, START, self.last_game)

    def chooseAction(self):
        _next_reward = 0
        action = ""
 
        if np.random.uniform(0,1) < self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            for action_ in self.actions:
                next_reward = self.state_values[self.State.nextPosition(action_)]
                if next_reward >= _next_reward:
                    action = action_
                    _next_reward = next_reward
        return action

    def takeAction(self, action):
        position = self.State.nextPosition(action)
        return State(state=position)
        
    def reset(self):
        self.states = []
        self.State = State()


