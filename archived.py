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