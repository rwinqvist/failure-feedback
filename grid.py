import numpy as np


LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

ACTION_NAMES = {LEFT: "left", DOWN: "down", RIGHT: "right", UP: "up"}

def generate_map(size):
    board = np.full((size, size), ".")
    board[0][0] = "S"
    board[-1][-1] = "G"

    return ["".join(x) for x in board]

class Grid(object):
    def __init__(self, size, slip_rate=2/3): 

        # SET UP STATE SPACE
        rows = cols = size 
        self.rows = rows 
        self.cols = cols
        self.num_states = num_states = rows * cols 
        self.states = [(row, col) for row in range(rows) for col in range(cols)]
        self.s0 = (0, 0)
        self.goal = (rows-1, cols-1)
        self.goal_states = [self.goal]
        self.action_names = ACTION_NAMES

        map = generate_map(size)
        self.map = np.asarray(map, dtype="c")
        self.decoded_map = np.array([[c.decode() for c in row] for row in self.map])

        # SET UP ACTION SPACE 
        self.num_actions = num_actions = 4 
        self.actions = np.arange(self.num_actions)
        self.slip_rate = slip_rate

        # SET UP TRANSITIONS AND REWARDS 
        self.T = np.zeros((num_states, num_actions, num_states))
        self.R_sas = np.zeros((num_states, num_actions, num_states))
        self.R_sa = np.zeros((num_states, num_actions))
        self.r_nom = -1
        self.r_goal = 10
        self.build_model()


    def build_model(self):
        success_rate = 1 - self.slip_rate

        for (sidx, state) in enumerate(self.states):
            if state == self.goal:
                self.T[sidx, :, sidx] = 1 
            else:
                for action in self.actions:
                    other_actions = self.get_other_actions(action)
                    for a in other_actions:
                        next_state = self.step(state, a)
                        next_sidx = self.states.index(next_state)   

                        p = success_rate if a == action else self.slip_rate/(len(other_actions)-1)
                        self.T[sidx, action, next_sidx] += p 
                    
                        r = self.r_goal if a == action and next_state == self.goal else self.r_nom
                        self.R_sas[sidx, action, next_sidx] = r
                    
        self.R_sa = np.multiply(self.T, self.R_sas).sum(axis=2)
                

    def step(self, state, action):
        row, col = state 

        if action == LEFT:
            col = max(col-1, 0)
        elif action == DOWN:
            row = min(row+1, self.rows-1)
        elif action == RIGHT: 
            col = min(col+1, self.cols-1)
        elif action == UP: 
            row = max(row-1, 0)

        return (row, col)
    

    def get_other_actions(self, action):
        other_actions = [(action - 1) % 4, action, (action + 1) % 4]
        return other_actions



if __name__ == "__main__":
    size = 2 

    grid = Grid(size)

    """
    for (sidx, state) in enumerate(grid.states): 
        for action in grid.actions: 
            print("\n\nState: ", state)
            print("Action: ", ACTION_NAMES[action])
            idxs = np.where(grid.T[sidx, action] != 0)[0]
            for idx in idxs: 
                print("Next: ", grid.states[idx], "\t p: ", grid.T[sidx, action, idx])
    """

    
    for (sidx, state) in enumerate(grid.states):
        for action in grid.actions: 
            print("\n\nState: ", state)
            print("Action: ", ACTION_NAMES[action])
            idxs = np.where(grid.T[sidx, action] != 0)[0]
            for idx in idxs: 
                print("Next: ", grid.states[idx], "\t p: ", grid.T[sidx, action, idx], "\t R: ", grid.R_sas[sidx, action, idx], "\t R2: ", grid.R_sa[sidx, action])
    

    