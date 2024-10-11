import numpy as np 
import random 
import logging 
from env_wrapper import EnvironmentWrapper

class MCOMDP_Planner(object): 
    def __init__(self, environment: EnvironmentWrapper, experiment_info, query_heuristic = "alg"): 
        logging.info("Initializing MCOMDP Planner...")

        self.environment = environment

        # States 
        self.states = environment.states 
        self.env_states = environment.env_states
        self.goal_states = environment.goal_states
        self.terminal_states = environment.terminal_states

        # Actions 
        self.actions = environment.actions 
        self.action_names = environment.action_names 

        # Severity levels 
        self.severity_levels = environment.severity_levels
        self.severity_map = environment.severity_map        
        self.min_sev, self.max_sev = min(self.severity_levels), max(self.severity_levels)
        self.max_acc_sev = environment.max_acc_sev

        # Dynamics
        self.T = environment.T 
        self.R = environment.R 
        self.O = environment.O 
        self.T_env = environment.T_env 
        self.T_sev = environment.T_sev 

        # hyperparams 
        self.recovery_rate = environment.recovery_rate
        self.query_cost = experiment_info["query_cost"]

        # Initialization 
        self.s0 = environment.s0 
        self.b0 = {0: 1}

        self.QMDP = environment.QMDP 
        self.VMDP = environment.VMDP 
        self.query_heuristic = query_heuristic

        logging.info("MCOMDP Planner initialized.\n")


    def run(self, num_episodes):
        """
        Run the MCOMDP planner for num_episodes episodes. 
        """
        logging.info("\nRunning MCOMDP planner...")

        rewards = np.zeros(num_episodes)
        severities = np.zeros(num_episodes)
        step_count = np.zeros(num_episodes)
        query_count = np.zeros(num_episodes)
        failure_count = np.zeros(num_episodes)
        query_states = [[] for i in range(num_episodes)]
        query_beliefs = [[] for i in range(num_episodes)]

        for episode in range(num_episodes): 
            log_msg = ""
            if episode % 100 == 0 or num_episodes < 10: 
                log_msg = f"{episode+1}/{num_episodes}"
                logging.info(f"* Running episode {log_msg}")
            rewards[episode], severities[episode], step_count[episode], query_count[episode], failure_count[episode], query_states[episode], query_beliefs[episode] = self.run_episode(episode)

        return rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs 
    


    def run_episode(self, episode, pick_query_before_execute=False):
        current_state = self.s0 
        current_belief = self.b0 
        done = False 

        total_reward = 0
        step_count = 0
        failure_count = 0 
        query_count = 0
        query_states = []
        query_beliefs = []
        accumulated_severity = 0    # for expert's score keeping 

        while not done: 
            current_env_state, current_acc_sev = current_state 
            #print("\nCurrent state: ", current_state)

            # pick best action 
            action = self.pick_action(current_env_state, current_belief)
            #print("Best action: ", action)

            # execute action 
            next_state, reward, severity, done = self.execute_action(current_state, action)
            #print("Next state: ", next_state)
            #print("Reward: ", reward) 
            #print("Severity: ", severity)
            #print("Done: ", done)

            if severity is not None: 
                #print("Failure occurred")
                # failure occurred 
                failure_count += 1 
                accumulated_severity = next_state[1]
                
                # get observation 
                observation = self.get_observation(current_state, action, next_state)
                #print("Observation")

                # update belief 
                next_belief = self.compute_next_belief(current_state, action, next_state, observation, current_belief)
                #print("Belief updated")

                if pick_query_before_execute:
                    # find condition for when to query based on old belief 
                    pass 

                else: 
                    # use new belief to determine query action 
                    if self.query_heuristic == "alg":
                        query = self.query_after_update(current_env_state, next_belief)
                        #print("Query: ", query)

                    elif self.query_heuristic == "always":
                        # always query
                        query = True 

                    else: 
                        # never query
                        query = False

                    #next_state = (current_env_state, next_state[1])

                if query: 
                    query_states.append(current_state)
                    query_beliefs.append(current_belief)
                    reward -= self.query_cost
                    next_belief = {accumulated_severity: 1}
                    query_count += 1 

            elif self.recovery_rate > 0:
                # successful execution and positive recovery rate
                next_belief = self.compute_recovery_belief(current_belief)

            else: 
                # successful execution but no recovery -> belief does not change
                next_belief = current_belief

            step_count += 1 
            total_reward += reward 
            current_state = next_state 
            current_belief = next_belief 
            #input()
        
        logging.debug(f"Episode {episode+1} finished.")
        return total_reward, accumulated_severity, step_count, query_count, failure_count, query_states, query_beliefs


    def pick_action(self, env_state, belief):
        """
        Pick best action according to current known state factor and current belief.
        """
        acc_sevs = list(belief.keys())

        if len(belief) == 1:
            # no uncertainty, just pick best action 
            state = (env_state, acc_sevs[0])
            sidx = self.states.index(state)
            optimal_actions = np.argmax(self.QMDP[sidx])

            if np.size(optimal_actions) == 1:
                optimal_action = int(optimal_actions)
            else: 
                optimal_action = int(np.random.choice(optimal_actions))

        else: 
            Q = np.zeros(len(self.actions))
            #print("Q: ", Q)
            for (acc_sev, p) in belief.items():
                state = (env_state, acc_sev)
                sidx = self.states.index(state)
                Q += p*self.QMDP[sidx] 

            Q_max = np.max(Q)
            filter = np.isclose(Q, Q_max)
            optimal_actions = np.array(self.actions)[filter]
            optimal_action = int(np.random.choice(optimal_actions))

        return optimal_action



    def execute_action(self, state, action):
        """
        Execute action.
        """
        logging.debug(f"In state {state}. Executing action {self.action_names[action]}...")
        env_state, acc_sev = state 
        sidx = self.states.index(state)
        state_idxs = np.arange(len(self.states))
        trans_probs = np.asarray(self.T[sidx, action]).astype("float64")
        trans_probs /= np.sum(trans_probs)

        next_sidx = random.choices(state_idxs, trans_probs)[0]
        next_state = next_env_state, next_acc_sev = self.states[next_sidx]

        severity = next_acc_sev - acc_sev 
        if severity > 0:
            logging.debug(f"Failed to execute action. Caused severity: {severity}")

        else:
            logging.debug("Action successfully executed.")
            severity = None 
        
        reward = self.R[sidx, action, next_sidx]
        done = True if next_state in self.goal_states or next_state in self.terminal_states else False 

        return next_state, reward, severity, done
    


    def get_observation(self, state, action, next_state): 
        logging.debug("Receiving observation...")
        sidx = self.states.index(state)
        next_sidx = self.states.index(next_state)

        obs_prob = np.asarray(self.O[sidx, action, next_sidx]).astype('float64')
        obs_prob /= np.sum(obs_prob)

        observation = np.random.choice(self.severity_levels, p=obs_prob)
        logging.debug(f"Observed severity level: {observation}")
        return observation
    


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
        next_acc_sevs = list(set([min(i+j, self.max_acc_sev) for i in current_acc_sevs for j in self.severity_levels]))
        next_belief = {}

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

            next_belief[next_acc_sev] = acc_belief 
            norm_const += acc_belief 

        next_belief.update((key, value/norm_const) for key, value in next_belief.items())

        return next_belief
    

    def compute_recovery_belief(self, belief): 
        recovery = 1
        recovery_belief = {}
        next_belief = {}

        for (acc_sev, p) in belief.items():
            new_acc_sev = max(acc_sev - recovery, 0)
            if new_acc_sev in recovery_belief:
                recovery_belief[new_acc_sev] += p
            else: 
                recovery_belief = p 

        all_acc_sevs = list(belief.keys()) + list(recovery_belief.keys())
        for acc_sev in all_acc_sevs:
            p = 0 
            if acc_sev in belief: 
                p += (1 - self.recovery_rate)*belief[acc_sev]
            if acc_sev in recovery_belief:
                p += self.recovery_rate*recovery_belief[acc_sev]

            next_belief[acc_sev] = p 

        belief_sum = np.sum(list(next_belief.values()))
        
        return next_belief
    

    def query_after_update(self, env_state, belief):
        """
        Determine whether to query or not.
        """
        logging.debug("Determining query action...")

        # best action if we don't query 
        next_action_nq = self.pick_action(env_state, belief)

        query_value = 0 

        #print("\nState: ", env_state)
        #print("Belief: ", belief)
        #print("Nq action: ", next_action_nq)

        # compute query value
        for (acc_sev, prob) in belief.items():
            state = (env_state, acc_sev)
            sidx = self.states.index(state)
            next_action_q = np.argmax(self.QMDP[sidx])
            query_value -= prob*self.QMDP[sidx, next_action_nq]
            query_value += prob*self.QMDP[sidx, next_action_q]
            #input()

        # compute expected return when not querying (for comparison only)
        for (acc_sev, prob) in belief.items(): 
            state = (env_state, acc_sev)
            sidx = self.states.index(state)
            q_val = prob*self.QMDP[sidx, next_action_nq]

        #print("\nquery value: ", query_value)
        #print("query cost: ", self.query_cost)
        #print("diff: ", query_value - self.query_cost)

        query = query_value >= self.query_cost
        #print(query)
        #input()

        if query > 0:
            #print(query_value - self.query_cost)
            #input()
            pass
            #print("Env state: ", env_state)
            #print("\nnext action not q: ", self.action_names[next_action_nq])
            #print("state: ", state)
            #print("Q: ", self.QMDP[sidx])
            #print("next action q: ", self.action_names[next_action_q])
            #print(f"Query value: {query_value}")
            #print(f"Query cost: {self.query_cost}")
            #print(f"Query: {query}")
            #input()

        return query
