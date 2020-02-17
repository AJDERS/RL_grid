import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt     
from matplotlib import colors
import matplotlib.patches as mpatches
from copy import deepcopy
import random as r

# TODO: Better plotting, Indicate if won, lost or out of actions, multiprocess Agent.play(), variable exploration rate.

class State:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros([rows, cols])        
        ### Define max capacity.
        self.action_cap = rows*cols

        ### Define walls
        self.walls = [(r.randrange(1, rows), r.randrange(1,cols)) for i in range(int(rows*cols*0.05))]
        for wall in self.walls:
           self.board[wall[0],wall[1]] = -1

        ### Start State
        self.state = (0,0)

        ### Win State
        self.win_state = (r.randrange(1, rows), r.randrange(1,cols))
        while self.win_state in self.walls:
            self.win_state = (r.randrange(1, rows), r.randrange(1,cols))       
        self.isEnd = False
        self.traps = self.defineTraps()        

    def defineTraps(self):
        wa = self.walls
        wi = [self.win_state]
        t = [(r.randrange(1, self.rows), r.randrange(1, self.cols)) for i in range(int(self.rows*self.cols*0.05))]
        t = list(set(t).difference(set(wa)).difference(set(wi)))
        return t
        

    def giveReward(self):
        map_size = self.rows*self.cols
        if self.state == self.win_state:
            return 5*map_size
        elif self.state in self.traps:
            return -map_size
        else:
            try:
               if self.state in self.state_values:
                   return -0.1*map_size
               else:
                   pass
            except:
               pass
        return 0.0

    def nextPosition(self, action):
        if action == "up":
            nextState = (self.state[0] - 1, self.state[1])
        elif action == "down":
            nextState = (self.state[0] + 1, self.state[1])
        elif action == "left":
            nextState = (self.state[0], self.state[1] - 1)
        else:
            nextState = (self.state[0], self.state[1] + 1)

        if (nextState[0] >= 0) and (nextState[0] <= self.rows-1):
            if (nextState[1] >= 0) and (nextState[1] <= self.cols-1):
                if nextState not in self.walls:
                    return nextState
        return self.state	               

    def isEndFunc(self, action_nr):
        action_cap = (action_nr >= self.action_cap)
        win = (self.state == self.win_state) 
        trap = (self.state in self.traps)
        if action_cap or win or trap:
            self.isEnd = True
        
class Agent: 
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.states = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State(rows, cols)
        self.lr = 0.2
        self.exp_rate = 0.3
        self.state_values = {}
        self.games = []
        for i in range(self.State.rows):
            for j in range(self.State.cols):
                self.state_values[(i,j)] = 0

    def play(self, rounds=10):
        i = 0
        action_nr = 0
        pbar = tqdm(total = rounds)
        while i < rounds:
            if self.State.isEnd:
                reward = self.State.giveReward()
                self.state_values[self.State.state] = reward
                for state in reversed(self.states):
                    reward = self.state_values[state] + self.lr * (reward - self.state_values[state])
                    self.state_values[state] = round(reward, 3)

                ### Append game, for plotting
                self.games.append(self.states)
                ### Go to next round, reset states and number of actions.
                self.reset()
                if i == rounds-1:
                    action_nr_last = action_nr
                i += 1
                action_nr = 0
                pbar.update(1)
            else:
                action = self.chooseAction()
                self.states.append(self.State.nextPosition(action))
                self.State = self.takeAction(action)

                ### Increment number of actions taken.
                action_nr += 1
                self.State.isEndFunc(action_nr)
        pbar.close()
        print("Last game: \n Reward: {} \n Last state: {} \n Win state: {} \n Number of actions: {} out of {}".format(reward, self.games[-1][-1], self.State.win_state, action_nr_last, self.State.action_cap))

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
        self.State.state = position
        return self.State
        
    def reset(self):
        self.states = []
        self.State.state = (0,0)
        self.State.isEnd = False

    def make_plot_data(self):
        start = (0,0)
        stop = self.State.win_state
        yx_traps = self.State.traps
        yx_walls = self.State.walls 
        data = np.zeros((self.rows, self.cols))
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) in yx_traps:
                    data[(i,j)] = -1.9
                elif (i,j) in yx_walls:
                    data[(i,j)] = 0.1
                elif (i,j) == start or (i,j) == stop:
                    data[(i,j)] = 1.9
                else:
                    data[(i,j)] = -0.1
        frames = []
        i=0
        for game in self.games[::1000]:
            frame = deepcopy(data)
            for point in game:
                if (point[0],point[1]) != (0,0):
                    frame[point[0]][point[1]] = 2.5
                frames.append((i*1000,deepcopy(frame)))
            i+=1
        return frames


    def plot_paths(self):
        # create discrete colormap
        colours = ['red', 'white', 'black', 'limegreen', 'cornflowerblue']
        cmap = colors.ListedColormap(colours)
        bounds = [-2,-1,0,1,2,3]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        patches = []
        legends = ['Traps', 'Not Visited', 'Walls', 'Start/Finish', 'Agent path']
 
        for i,_ in enumerate(colours):
            patch = mpatches.Patch(color=colours[i], label=legends[i])
            patches.append(patch)

        frames = self.make_plot_data()
        finished_frames = []
        for frame in tqdm(frames):
            fig, ax = plt.subplots()
            fig.set_size_inches(7.5,5) 
            ax.imshow(frame[1], cmap=cmap, norm=norm)

            # draw gridlines
            ax.grid(which='both', axis='both', linestyle='-', color='k', linewidth=2)
            ax.set_xticks(np.arange(-.5, 10, 1))
            ax.set_yticks(np.arange(-.5, 10, 1))
            ax.set_yticklabels([])
            ax.set_xticklabels([])                               
            plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
            plt.title('Path for game {} out of {}.'.format(frame[0], len(self.games)))
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,)) 
            finished_frames.append(image)
            plt.close()
        return finished_frames
             

         #fig = plt.figure(figsize=(8,8),dpi=100)
         #ax = fig.add_subplot(111)
         
         #ax.plot(x_traps, y_traps, c='red', linestyle="None", marker='x')
         #ax.plot(x_walls, y_walls, c='black', linestyle="None", marker='s')
         #ax.plot(start[1], start[0],c='green', ms=5.0, marker='o')
         #ax.plot(stop[1], stop[0],c='green', ms=7.5, marker='*')
         #ax.set(xlim=(-0.5, self.State.cols+.5),ylim=(-.5,self.State.rows+.5))
         #spacing = 1         
         #minorLocator = plt.MultipleLocator(spacing)
         #ax.yaxis.set_minor_locator(minorLocator)
         #ax.xaxis.set_minor_locator(minorLocator)
         #ax.grid(which = 'minor')
           
