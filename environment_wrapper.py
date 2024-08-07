import numpy as np
import math
import itertools 
import logging 
from fractions import Fraction

class EnvironmentWrapper(object):
    def __init__(self, environment, experiment_info):
        logging.info("\nWrapping environment...")
        self.environment = environment

        # env states and actions
        self.env_states = environment.states 
        self.env_s0 = environment.s0
        self.forbidden_env_states = environment.forbidden_states 
        self.actions = environment.actions
        self.action_names = environment.action_names 
        self.action_info = environment.action_info 

        # severity info 
        self.severity_levels = environment.severity_levels
        self.severity_map = environment.severity_map 
        self.num_sev_lvls = len(self.severity_levels)
        self.max_sev, self.min_sev = max(self.severity_levels), min(self.severity_levels)
        self.halt_sev = experiment_info["halt_factor"]*self.max_sev
        self.recovery_rate = experiment_info["recovery_rate"]

        # set state space 
        self.states = []
        self.terminal_states = []
        self.goal_states = []
        self.halting_states = []
        self.s0 = (self.env_s0, 0)
        self.set_state_space()

        # dynamics, rewards and observations 
        self.num_states = num_states = len(self.states)
        self.num_actions = num_actions = len(self.actions)
        num_env_states = len(self.env_states)
        num_sev_lvls = len(self.severity_levels)

        self.true_obs_prob = experiment_info["true_obs_prob"]
        self.severity_penalty_weight = experiment_info["severity_penalty_weight"]


        self.T_env = environment.T
        self.T = np.zeros((num_states, num_actions, num_states))
        self.T_sev = np.zeros((num_env_states, num_actions, num_env_states, num_sev_lvls))
        self.R_env = environment.R 
        self.R = np.zeros((num_states, num_actions, num_states))
        self.O = np.zeros((num_states, num_actions, num_states, num_sev_lvls))

        self.fill_tables()

        self.QMDP = None 
        self.VMDP = None 
        logging.info("Environment wrapped.")


    def set_VMDP(self, V):
        self.VMDP = V

    def set_QMDP(self, Q):
        self.QMDP = Q  
        

    def set_state_space(self):
        logging.debug("Setting state space.")
        states = []
        goal_states = []
        halting_states = []
        
        for env_state in self.env_states:
            for acc_sev in range(0, self.halt_sev+1):
                state = (env_state, acc_sev)
                states.append(state)

                if env_state in self.environment.goal_states:
                    goal_states.append(state)
                elif acc_sev == self.halt_sev:
                    halting_states.append(state)

        self.states = states 
        self.goal_states = goal_states
        self.halting_states = halting_states


    def fill_tables(self):
        self.fill_Tsev()
        self.fill_T()
        self.fill_R()
        self.fill_O()


    def fill_Tsev(self):
        for (sidx, state) in enumerate(self.states):
            env_idx = self.env_states.index(state[0])
            
            for action in self.actions: 
                sev_skew_factor = self.action_info[action]["skew_factor"]

                next_env_idxs = np.where(self.T_env[env_idx, action] != 0)[0]
                for next_env_idx in next_env_idxs:
                    next_env_state = self.env_states[next_env_idx]

                    if next_env_state in self.forbidden_env_states:
                        sev_probs = np.array(self.severity_map[next_env_state])*np.array([(sev_skew_factor**i) for i in range(self.num_sev_lvls)])
                        sev_probs = np.asarray(sev_probs).astype("float64")/np.sum(sev_probs)

                        self.T_sev[env_idx, action, next_env_idx] = sev_probs


    def fill_T(self):
        for (sidx, state) in enumerate(self.states):
            env_state, acc_sev = state 
            env_idx = self.env_states.index(env_state)

            if state in self.goal_states or state in self.terminal_states:
                self.T[sidx, :, sidx] = 1 
            
            elif state in self.halting_states:
                self.T[sidx, :, sidx] = 1 - self.recovery_rate
                next_state_rec = (env_state, acc_sev-1)
                next_sidx = self.states.index(next_state_rec)
                self.T[sidx, :, next_sidx] = self.recovery_rate

            else: 
                for action in self.actions: 
                    alt_actions = self.get_alt_actions(action)

                    success_rate = self.action_info[action]["success_rate"]
                    decline_factor = self.action_info[action]["performance_decline_factor"]**acc_sev 
                    p_success = decline_factor*success_rate
                    p_fail = (1 - p_success)/(len(alt_actions) - 1) 

                    for active_action in alt_actions:
                        if active_action == action: 
                            action_succeeded = True 
                            p_env = p_success 
                        else: 
                            action_succeeded = False 
                            p_env = p_fail 

                        next_env_state = self.get_next_env_state(state, active_action)
                        next_env_idx = self.env_states.index(next_env_state)

                        # NOTE THAT THIS ONLY WORKS WHEN FAILING AN ACTION LEADS TO A FORBIDDEN STATE
                        if next_env_state in self.forbidden_env_states:
                            # ENDED UP IN FORBIDDEN STATE 
                            # ADDED SEVERITY 
                            for (sev_idx, sev_lvl) in enumerate(self.severity_levels):
                                next_acc_sev = min(acc_sev+sev_lvl, self.halt_sev)

                                p_sev = self.T_sev[env_idx, action, next_env_idx][sev_idx]
                                next_state = (env_state, next_acc_sev)
                                next_sidx = self.states.index(next_state)
                                self.T[sidx, action, next_sidx] += np.array(p_env*p_sev)

                        else:
                            # ENDED UP IN ALLOWED STATE - NO ADDED SEVERITY 
                            # POSSIBLY ALSO RECOVERED 

                            recovery_rate = 0
                            next_state = (next_env_state, acc_sev) 
                            next_sidx = self.states.index(next_state)


                            if acc_sev >= 1 and action_succeeded:
                                recovery_rate = self.recovery_rate
                                next_state_rec = (next_env_state, acc_sev-1)
                                next_sidx_rec = self.states.index(next_state_rec)
                                self.T[sidx, action, next_sidx_rec] += p_env*recovery_rate

                            self.T[sidx, action, next_sidx] += p_env*(1-recovery_rate)
                    """
                    if state[0][0] == 1:
                        non_zero_idxs = np.nonzero(self.T[sidx, action])[0]
                        print("State: ", state)
                        print("Action: ", self.action_names[action])
                        print("T: ")
                        for i in non_zero_idxs:
                            ns = self.states[i]
                            p = self.T[sidx, action][i]
                            print("next state: ", ns, "\tp: ", p)
                        input()
                        
                        sum = np.sum(self.T[sidx, action])
                        if not np.isclose(sum,1):
                            print
                            print("sum: ", np.sum(self.T[sidx, action]))
                            input()
                    """


    def fill_R(self):
        for (sidx, state) in enumerate(self.states):
            env_state, acc_sev = state 
            env_idx = self.env_states.index(env_state)

            if state in self.goal_states:
                r_goal = self.R_env[env_idx, :, env_idx][0]
                self.R[sidx] = r_goal - self.severity_penalty(acc_sev)

            elif state in self.terminal_states:
                self.R[sidx] = -self.severity_penalty(acc_sev)

            else: 
                for action in self.actions: 
                   next_idxs = np.where(self.T[sidx, action] != 0)[0]
                   for next_idx in next_idxs:
                    next_state = self.states[next_idx]

                    if next_state in self.goal_states:
                        self.R[sidx, action, next_idx] = max(self.R_env[env_idx, action])
                    else:
                        self.R[sidx, action, next_idx] = min(self.R_env[env_idx, action])


    def fill_O(self):
        for (sidx, state) in enumerate(self.states):
            env_state, acc_sev = state 

            if state not in self.goal_states and state not in self.terminal_states:
                for action in self.actions:
                    failure_states = []
                    next_state_idxs = np.where(self.T[sidx, action] != 0)[0]
                    for next_sidx in next_state_idxs:
                        next_state = next_env_state, next_acc_sev = self.states[next_sidx]
                        if next_acc_sev > acc_sev: 
                            failure_states.append(next_state)

                    for fail_state in failure_states:
                        next_sidx = self.states.index(fail_state)
                        next_acc_sev = fail_state[1]

                        true_sev_lvl = next_acc_sev - acc_sev 
                        true_sev_idx = self.severity_levels.index(true_sev_lvl)

                        wrong_obs_prob = (1 - self.true_obs_prob)/(self.num_sev_lvls - 1)
                        obs_probs = wrong_obs_prob*np.ones(self.num_sev_lvls)
                        obs_probs[true_sev_idx] = self.true_obs_prob
                        #print("O: ", obs_probs)
                        self.O[sidx, action, next_sidx] = obs_probs 
 

    def get_next_env_state(self, state, action):
        env_state = state[0]
        if action in self.action_info:
            direction = self.action_info[action]["direction"]
        else:
            direction = action
        next_env_state = self.environment.get_next_state(env_state, direction)
        return next_env_state
    

    def get_alt_actions(self, action):
        alt_actions = self.environment.get_alt_actions(action)
        return alt_actions


    def severity_penalty(self, acc_sev):
        return acc_sev*self.severity_penalty_weight