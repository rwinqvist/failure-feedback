import numpy as np 
import math 
import logging 


class ValueIteration(object):
    def __init__(self, environment, action_names=None):
        self.states = environment.states 
        self.actions = environment.actions 
        self.s0 = environment.s0
        self.goal_states = environment.goal_states 
        self.terminal_states = environment.terminal_states
        self.T = environment.T 
        self.R = environment.R 
        self.env = environment

    def run(self, max_iter=1000, threshold=0.001, gamma=0.9):
        logging.info("\nSolving MDP using Value Iteration algorithm...")
        delta = 2*threshold 
        Q = np.zeros((len(self.states), len(self.actions)))

        for state in self.terminal_states + self.goal_states:
            sidx = self.states.index(state)
            r = self.R[sidx, :, sidx]
            Q[sidx, :] = np.asarray(r)

        policy = {}
        V = np.zeros(len(self.states))

        i = 0
        states = list(set(self.states) - set(self.goal_states) - set(self.terminal_states))
        
        while delta > threshold and i < max_iter:
            if i % 10 == 0:
                logging.debug(f"Iteration number: {i+1} \t Delta: {delta}")
            
            delta = 0 
            for state in states:
                sidx = self.states.index(state)
                q_max = -math.inf 
                a_opt = None 

                for action in self.actions:
                    q = 0
                    trans_probs = self.T[sidx, action]
                    for (next_sidx, p) in enumerate(trans_probs):
                        r = self.R[sidx, action, next_sidx]
                        q += p*(r + gamma*V[next_sidx])

                    if q > q_max:
                        q_max = q 
                        a_opt = action 

                    Q[sidx, action] = q 

                delta = max(delta, abs(q_max - V[sidx]))
                V[sidx] = q_max 

                policy[state] = a_opt 

            i += 1

        if i >= max_iter:
            logging.info("Value iteration terminated. Maximum number of iterations exceeded.")
            logging.debug(f"Delta: {delta}")
        else:
            logging.info("Value iteration terminated. Convergence reached.")

        logging.info("MDP solved.")
        return V, Q, policy
