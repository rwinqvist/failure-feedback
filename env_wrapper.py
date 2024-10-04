import numpy as np 
import logging 
from fractions import Fraction 

class EnvironmentWrapper(object): 
    def __init__(self, environment, exp_info): 
        logging.info("Wrapping environment...")
        self.environment = environment

        # env states
        self.env_states = environment.states 
        self.env_s0 = environment.s0 
        env_size = environment.size  

        # actions 
        self.actions = environment.actions 
        self.action_names = environment.action_names
        self.action_info = environment.action_info

        # severity info 
        self.severity_levels = environment.severity_levels
        self.max_sev = max(self.severity_levels)
        self.severity_map = environment.severity_map 
        self.num_sev_lvls = num_sev_lvls = len(self.severity_levels)
        self.recovery_rate = exp_info["recovery_rate"]
        if exp_info["max_acc_sev"] is not None: 
            self.max_acc_sev = exp_info["max_acc_sev"]
        else: 
            self.max_acc_sev = self.max_sev*env_size 

        
        # build state space 
        self.states = [] 
        self.terminal_states = []
        self.goal_states = []
        self.bouncing_states = []
        self.s0 = (self.env_s0, 0)      # default initialization. feel free to modify this, or do MC simulations starting from different s0's
        self.build_state_space() 

        # dynamics, rewards and observations 
        self.num_states = num_states = len(self.states)
        self.num_actions = num_actions = len(self.actions)

        self.true_obs_prob = exp_info["true_obs_prob"]
        self.severity_penalty_weight = exp_info["severity_penalty_weight"]

        self.T_env = environment.T
        self.T = np.zeros((num_states, num_actions, num_states))
        self.T_sev = environment.T_sev 
        self.R_env = environment.R 
        self.R = np.zeros((num_states, num_actions, num_states))
        self.O = np.zeros((num_states, num_actions, num_states, num_sev_lvls))

        self.build_pomdp() 
        self.R_sas = self.R 

        self.QMDP = None 
        self.VMDP = None 
        logging.info("Environment wrapped.")



    def build_state_space(self):
        """
        Build the state space by combining the environmental states with severity levels. A state is represented by a tuple (x, z), where x
        is the environmental state factor, and z the total accumulated severity.
        """
        logging.debug("Building state space.")
        states, goal_states, terminal_states, bouncing_states = [], [], [], []

        for env_state in self.env_states:
            if env_state not in self.environment.bouncing_states:
                for acc_sev in range(0, self.max_acc_sev+1):
                    state = (env_state, acc_sev)
                    states.append(state)

                    if env_state in self.environment.goal_states:
                        goal_states.append(state)
                    elif acc_sev >= self.max_acc_sev:
                        terminal_states.append(state)

        self.states = states 
        self.goal_states = goal_states
        self.terminal_states = terminal_states 
        
        logging.debug("State space built.")


    def build_pomdp(self): 
        self.build_dynamics()
        self.build_observation_matrix()

        #state = ((1, 0), 1)
        #self.build_dynamics_print(state)
        #self.build_transition_matrix()
        #self.build_reward_matrix()


    def build_dynamics(self):
        """
        Build transition matrix T(s,a,s) using the transition function of the underlying environment T_env(s_env, a, s_env) and the severity
        transitions T_sev(s_env, a, s_env, sev_lvl).

        NOTE: This setup assumes that every action failure leads to accumulation of severity
        """
        penalty_transitions = []
        for (sidx, state) in enumerate(self.states):
            #print("\n\nState: ", state)
            env_state, acc_sev = state 
            env_idx = self.env_states.index(env_state)

            if state in self.goal_states or state in self.terminal_states:
                self.T[sidx, :, sidx] = 1 

            else: 
                for action in self.actions: 
                    #print("Action: ", action)
                    p_success = self.action_info[action]["success_rate"]
                    performance_decline_factor = self.action_info[action]["performance_decline_factor"]
                    p_success *= performance_decline_factor
                    failure_transitions = self.environment.failure_transitions[env_state][action]
                    p_fail = (1 - p_success)/(len(failure_transitions))

                    next_env_idxs = np.where(self.T_env[env_idx, action] != 0)[0]
                    for next_env_idx in next_env_idxs:
                        next_env_state = self.env_states[next_env_idx]
                        reward = self.R_env[env_idx, action, next_env_idx]

                        if next_env_state in failure_transitions:
                            # failure occurred 
                            #print("Failure occurred!")
                            if next_env_state in self.environment.bouncing_states:
                                next_env_state = self.environment.bounce_state(next_env_state)
                            
                            for (sev_idx, sev_lvl) in enumerate(self.severity_levels):
                                p_sev = self.T_sev[env_idx, action, next_env_idx, sev_idx]
                                next_acc_sev = min(acc_sev+sev_lvl, self.max_acc_sev)
                                next_state = (next_env_state, next_acc_sev)
                                next_sidx = self.states.index(next_state)
                                self.T[sidx, action, next_sidx] += p_fail*p_sev                             
                                
                                transition = (sidx, action, next_sidx)
                                if next_state in self.terminal_states and transition not in penalty_transitions:
                                    penalty_transitions.append(transition)

                                if self.R[sidx, action, next_sidx] == 0:
                                    self.R[sidx, action, next_sidx] = reward
                                #print("Next state: ", next_state, "p: ", self.T[sidx, action, next_sidx], "r: ", reward)  

                        else: 
                            # action executed successfully
                            if acc_sev == 0: 
                                next_state = (next_env_state, acc_sev)
                                next_sidx = self.states.index(next_state)
                                self.T[sidx, action, next_sidx] += p_success
                                transition = (sidx, action, next_sidx)
                                if next_state in self.goal_states and transition not in penalty_transitions:
                                    penalty_transitions.append(transition) 

                            else:
                                # recovery
                                next_state = (next_env_state, acc_sev-1)
                                next_sidx = self.states.index(next_state)
                                self.T[sidx, action, next_sidx] += p_success*self.recovery_rate
                                transition = (sidx, action, next_sidx)
                                if next_state in self.goal_states and transition not in penalty_transitions:
                                    penalty_transitions.append(transition)

                                # no recovery
                                next_state = (next_env_state, acc_sev)
                                next_sidx = self.states.index(next_state)
                                self.T[sidx, action, next_sidx] += p_success*(1 - self.recovery_rate)
                                transition = (sidx, action, next_sidx)
                                if next_state in self.goal_states and transition not in penalty_transitions:
                                    penalty_transitions.append(transition)

                            self.R[sidx, action, next_sidx] = reward


        for transition in penalty_transitions:
            sidx, action, next_sidx = transition 
            next_state = self.states[next_sidx]
            acc_sev = next_state[1]
            penalty = self.get_severity_penalty(next_state[1])
            self.R[sidx, action, next_sidx] += penalty


    def build_observation_matrix(self): 
        for (sidx, state) in enumerate(self.states):
            _, acc_sev = state 

            if state not in self.goal_states and state not in self.terminal_states:
                for action in self.actions: 
                    next_state_idxs = np.where(self.T[sidx, action] != 0)[0]
                    for next_state_idx in next_state_idxs:
                        next_state = _, next_acc_sev = self.states[next_state_idx]

                        # we only need to add observation if the transition is a failure transition 
                        sev_diff = next_acc_sev - acc_sev 
                        if sev_diff > 0:
                            next_sidx = self.states.index(next_state)

                            if next_acc_sev < self.max_acc_sev or next_acc_sev == self.max_acc_sev and sev_diff == self.max_sev:
                                true_sev_idx = self.severity_levels.index(sev_diff)
                                wrong_obs_prob = (1 - self.true_obs_prob)/(self.num_sev_lvls - 1)
                                obs_probs = wrong_obs_prob*np.ones(self.num_sev_lvls)
                                obs_probs[true_sev_idx] = self.true_obs_prob
                                self.O[sidx, action, next_sidx] = obs_probs 
                        
                            else:
                                # multiple possible severity degrees may have occurred 
                                possible_sevs = [i for i in self.severity_levels if i >= sev_diff]

                                for (sev_idx, sev_lvl) in enumerate(self.severity_levels):
                                    if sev_lvl in possible_sevs:
                                        p = self.true_obs_prob/len(possible_sevs) + wrong_obs_prob/self.num_sev_lvls

                                    else:
                                        p = wrong_obs_prob/self.num_sev_lvls
                                    
                                    self.O[sidx, action, next_sidx, sev_idx] = p



    def get_severity_penalty(self, acc_sev):
        return -self.severity_penalty_weight*acc_sev
    

    def set_QMDP(self, Q):
        self.QMDP = Q 

    def set_VMDP(self, V): 
        self.VMDP = V