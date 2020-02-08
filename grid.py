
BOARD_ROWS = 3
BOARD_COLS = 4
HOLES = (1,1)
WIN_STATE = (0,3)
LOSE_STATE = (2,0)
START = (2,0)
DETERMINISTIC = True

class State():
    def __init__(self, state=START):
        self.board = self.defineHoles(HOLES)
        self.state = START
        self.isEnd = False
        self.determine = DETERMINISTIC

    def defineHoles(holes):
        board = np.zeros([BOARD_ROWS, BOARD_COLS])
        for hole in holes:
           board[hole[0],hole[1]] = -1
        return board

    def giveReward():
        if self.state == WIN_STATE:
            return 1
        elif self.state == LOSE_STATE:
            return -1
        else:
            return 0

    def nextPosition(self, action):
        if self.determine:
            if action == "up":
                nextState = (self.state[0] - 1, self.state[1])
            if action == "down":
                nextState = (self.state[0] + 1, self.state[1])
            if action == "left":
                nextState = (self.state[0], self.state[1] - 1)
            else:
                nextState = (self.state[0], self.state[1] + 1)

        if (nextState[0] >= 0) and (nextState[0] < BOARD_ROWS):
            if (nextState[1] >= 0) and (nextState[1] < BOARD_COLS):
                if all([nextState != hole for hole in HOLES]):
                    return nextState
        return self.state	               

def Agent()
    
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

    def play(self, round=10):
        i = 0
        while i < round:
            if self.State.isEnd:
                reward = self.State.giveReward()
                self.state_values[self.State.state] = reward
                print("GAME OVER", reward)



    


