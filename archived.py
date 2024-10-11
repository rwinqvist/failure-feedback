def build_dynamics_print(self, check_state=None):
    """
    Build transition matrix T(s,a,s) using the transition function of the underlying environment T_env(s_env, a, s_env) and the severity
    transitions T_sev(s_env, a, s_env, sev_lvl).

    NOTE: This setup assumes that every action failure leads to accumulation of severity
    """
    for (sidx, state) in enumerate(self.states):
        condition = state == check_state
        print(condition)
        print("\n\nState: ", state) if condition else None
        env_state, acc_sev = state 
        env_idx = self.env_states.index(env_state)

        if state in self.goal_states or state in self.terminal_states:
            self.T[sidx, :, sidx] = 1 

        else: 
            for action in self.actions: 
                print("Action: ", action) if condition else None
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
                        print("Failure occurred!") if condition else None
                        if next_env_state in self.environment.bouncing_states:
                            next_env_state = self.environment.bounce_state(next_env_state)
                        
                        for (sev_idx, sev_lvl) in enumerate(self.severity_levels):
                            p_sev = self.T_sev[env_idx, action, next_env_idx, sev_idx]
                            next_acc_sev = min(acc_sev+sev_lvl, self.max_acc_sev)
                            next_state = (next_env_state, next_acc_sev)
                            next_sidx = self.states.index(next_state)
                            self.T[sidx, action, next_sidx] += p_fail*p_sev                             
                            
                            if next_state in self.goal_states or next_state in self.terminal_states:
                                reward += self.get_severity_penalty(next_acc_sev)

                            self.R[sidx, action, next_sidx] = reward
                            print("Next state: ", next_state, "p: ", self.T[sidx, action, next_sidx], "r: ", reward) if condition else None  

                    else: 
                        # action executed successfully
                        print("Success!!!") if condition else None
                        if acc_sev == 0: 
                            next_state = (next_env_state, acc_sev)
                            next_sidx = self.states.index(next_state)
                            self.T[sidx, action, next_sidx] += p_success 
                            print("Acc sev 0 so next state: ", next_state, "p: ", self.T[sidx, action, next_sidx], "r: ", reward) if condition else None
                        
                        else:
                            #print("\n\nSuccess!!!!")
                            #print("State: ", state)
                            #print("Action: ", action)
                            # recovery
                            next_state = (next_env_state, acc_sev-1)
                            next_sidx = self.states.index(next_state)
                            self.T[sidx, action, next_sidx] += p_success*self.recovery_rate
                            print("Recovery state: ", next_state, "p: ", p_success*self.recovery_rate) if condition else None

                            # no recovery
                            next_state = (next_env_state, acc_sev)
                            next_sidx = self.states.index(next_state)
                            self.T[sidx, action, next_sidx] += p_success*(1 - self.recovery_rate)
                            print("No recovery state: ", next_state, "p: ", p_success*(1 - self.recovery_rate)) if condition else None
                            #input()

                        self.R[sidx, action, next_sidx] = reward
                input() if condition else None











                for action in self.actions: 
                    #print("Action: ", action)
                    p_success = self.action_info[action]["success_rate"]

                    performance_factor = self.get_performance_factor(action, acc_sev)
                    #performance_decline_factor = self.action_info[action]["performance_decline_factor"]

                    #print("\nState: ", state, "Action: ", action, "p_success: ", p_success, "p_success: ", p_success*performance_factor)
                    #input()
                    p_success = p_success*performance_factor
                    #perturbation = self.perturb_success_rate(action, acc_sev)

                    #print("p_success: ", p_success)
                    #print("perturbation: ", perturbation)
                    #print(perturbation*p_success)
                    #print("Action: ", action, "p_success: ", self.action_info[action]["success_rate"], "p_success: ",  min(1, perturbation*p_success))
                    #print("\nAction: ", action, "p_success: ", p_success)
                    #input()

                   # p_success = min(1, perturbation*p_success)
  

                    #severity_penalty_factor = (1 - ((self.max_acc_sev-acc_sev)/self.max_acc_sev))
                    #print("\naction: ", action)
                    #print("penalty: ", severity_penalty_factor)
                    #p_success *= performance_decline_factor
                    #p_success *= performance_decline_factor*severity_penalty_factor

                    #exponential = math.exp(-performance_decline_factor*acc_sev*(action+1))
                    #print("factor: ", math.exp(-exponential))
                    #p_success = p_success*math.exp(self.alpha*-exponential)
                    #print("p_success: ", self.action_info[action]["success_rate"], "p_success: ", p_success)
                    #input()
                   
                    #print("Action: ", self.action_names[action], "p_success: ", p_success)






# USE FOR PRINTOUTS
def compute_next_belief(self, state, action, next_state, observation, belief):
        """
        Compute next belief based on current state, action and belief. 
        """
        logging.debug("\nComputing next belief...")

        env_state, acc_sev = state 
        sidx = self.states.index(state)
        oidx = self.severity_levels.index(observation)
        next_env_state, _ = next_state 

        current_acc_sevs = list(belief.keys())

        #print("\nCurrent belief: ", belief)
        #print("State: ", state)
        #print("Action: ", self.action_names[action])
        #print("Next state: ", next_state)
        #print("Observation: ", observation)
        #print("O: ", np.where(self.O[sidx, action] != 0))
        #T = self.T[sidx, action]
        #for (tidx, t) in enumerate(T): 
            #if (t != 0):
                 #print(f"State: {self.states[tidx]}, p: {t}")
        #print("Current acc sevs: ", current_acc_sevs)
        #input()

        next_acc_sevs = list(set([min(i+j, self.max_acc_sev) for i in current_acc_sevs for j in self.severity_levels]))
        next_belief = {}

        #print("severity levels: ", self.severity_levels)
        #print("next acc sevs: ", next_acc_sevs)

        norm_const = 0 
        for next_acc_sev in next_acc_sevs: 
            s_next = (next_env_state, next_acc_sev)
            next_sidx = self.states.index(s_next)
            acc_belief = 0 
            for current_acc_sev in current_acc_sevs:
                s = (env_state, current_acc_sev)
                sidx = self.states.index(s)
                obs_prob = self.O[sidx, action, next_sidx, oidx]
                trans_prob = self.T[sidx, action, next_sidx]
                ind_belief = belief[current_acc_sev]*obs_prob*trans_prob

                acc_belief += ind_belief 

                #print("\nState: ", s)
                #print("Action: ", self.action_names[action])
                #print("Next: ", s_next)
                #print("Obs: ", observation)
                #print("Obs prob: ", obs_prob)
                #print("T: ", trans_prob)
                #print("current belief: ", belief[current_acc_sev])
                #print("next belief: ", ind_belief)
                #print("acc belief: ", acc_belief)
                #input()

            next_belief[next_acc_sev] = acc_belief 
            norm_const += acc_belief 

        next_belief.update((key, value/norm_const) for key, value in next_belief.items())
        belief_sum = sum(list(next_belief.values()))

        if not np.isclose(belief_sum, 1):
            print("belief does not sum to 1!!!!!")
            input()
        #print(next_belief)
        #print("belief sums to: ",  belief_sum)
        #input()

        return next_belief