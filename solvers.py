import numpy as np
import math
from grid import Grid 
import logging

class ValueIteration(object):
    def __init__(self, env):
        self.env = env 
        self.all_states = env.states 
        self.goal_states = env.goal_states
        self.terminal_states = env.terminal_states
        self.actions = env.actions
        self.T = env.T 
        self.R = env.R_sas

        self.states = list(set(self.all_states) - set(self.goal_states) - set(self.terminal_states))
        self.goal_terminal = list(set(self.goal_states).union(set(self.terminal_states)))


    def run(self, max_iter=500, threshold=0.01, gamma=0.99):
        delta = math.inf
        Q = np.zeros((len(self.all_states), len(self.actions)))
        V = np.zeros((max_iter+1, len(self.all_states)))

        for state in self.goal_terminal:
            sidx = self.all_states.index(state)
            V[:, sidx] = self.R[sidx, 0, sidx]

        policy = {}

        k = 1
        while delta > threshold and k <= max_iter:
            #print("k: ", k, "delta: ", delta)
            delta = 0
            for state in self.states:
                #gamma = self.get_discount_factor(state[1])
                sidx = self.all_states.index(state)
                for action in self.actions: 
                    q = 0
                    next_sidxs = np.where(self.T[sidx, action] != 0)[0]
                    for next_sidx in next_sidxs: 
                        p = self.T[sidx, action, next_sidx]
                        r = self.R[sidx, action, next_sidx]
                        #print("next sidx: ", next_sidx)
                        q += p*(r + gamma*V[k-1, next_sidx])

                        #next_state = self.all_states[next_sidx]
                        #if next_state in self.goal_states:
                            #print("\ngoal state: ", next_state)
                            #print("r: ", r)
                            #print("q: ", q)
                            #input()
                        
                        """
                        if k > 1:
                            if q == 0:
                                print("\nState: ", state)
                                print("Action: ", action)
                                print("Next: ", self.states[next_sidx])
                                print("p: ", p)
                                print("q: ", q)
                                input()
                        """
                    Q[sidx, action] = q 
                v = np.max(Q[sidx])
                V[k, sidx] = v
                delta = max(delta, abs(v - V[k-1, sidx]))
                policy[state] = np.argmax(Q[sidx])

            k += 1

        return V, Q, policy




if __name__ == "__main__":
    grid = Grid(3)
    print(grid.decoded_map)
    vi = ValueIteration(grid)
    V, Q, policy = vi.run()

    for (sidx, state) in enumerate(grid.states):
        print("\nState: ", state)
        print("Action: ", grid.action_names[policy[state]])
        print("Q :", Q[sidx])
    





    