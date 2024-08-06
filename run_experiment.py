import numpy as np 
import logging
from rocky_road import RockyRoad
from mdp_solvers import ValueIteration
from environment_wrapper import EnvironmentWrapper
from mcomdp_planner import MCOMDP_Planner

ENV_INFO = {
    "terrains": ["A", "C", "R", "L", "P"],
    "severities": [1, 2, 3, 4, 5],

    "A": {
        "type": "allowed",
        "p": 1,
    },

    "C": {
        "type": "allowed",
        "p": 0,
    },

    "R": {
        "type": "forbidden",
        #"p": 0.4,
        "p": 1/3,
        "nom_sev_probs": ["0.1", "0.15", "0.2", "0.25", "0.3"],
    },

    "L": {
        "type": "forbidden",
        #"p": 0.4,
        "p": 1/3,
        "nom_sev_probs": ["0.25", "0.25", "0.2", "0.2", "0.1"],
    },

    "P": {
        "type": "forbidden",
        #"p": 0.2,
        "p": 1/3,
        "nom_sev_probs": ["0.25", "0.25", "0.2", "0.2", "0.1"],
    }
}


EXP_INFO = {
    "true_obs_prob": 0.5,             
    "query_cost": 10,
    "acc_sev_penalty_weight": 10,
    "recovery_rate": 0.2,
    "severities": [1, 2, 3, 4, 5],
}


def main():
    num_runs = 1
    num_episodes = 1

    for i in range(num_runs):
        length = 10
        env_info = ENV_INFO
        severity_levels = env_info["severities"]
        recovery_rate = EXP_INFO["recovery_rate"]
        halt_sev = 5

        rr = RockyRoad(length, env_info, use_preset_map=False, is_uneven=True)
        print("Map: \n", rr.map, "\n\n")
        rr.print_action_info()

        alg = ValueIteration(rr)
        V, Q, policy = alg.run()

    
        env = EnvironmentWrapper(rr, severity_levels, halt_sev, recovery_rate)

        alg = ValueIteration(env)
        V, Q, policy = alg.run()

        env.set_VMDP(V)
        env.set_QMDP(Q)

        planner = MCOMDP_Planner(env)
        planner.run(num_episodes)

        """
        for state in env.states:
            if state[0][0] == 1:
                sidx = env.states.index(state)
                if state in policy:
                    print("\nState: ", state)
                    print("Q: ", Q[sidx])
                    print("Policy: ", rr.action_names[policy[state]])
                    input() 
        """

        """
        for (sidx,state) in enumerate(env.states): 
            env_state, acc_sev = state 
            env_idx = rr.states.index(env_state)
            for action in rr.actions: 
                if state[0][0] == 1:
                    print("\nState: ", state)
                    print("Action: ", rr.action_names[action])
                    ridxs = np.where(env.R[sidx, action] != 0)[0]
                    for ridx in ridxs:
                        print("Next state: ", env.states[ridx])
                        print("Reward: ", env.R[sidx, action, ridx])
                        print("rr reward: ", rr.R[env_idx, action])
                    input()
        exit()
        """
        """
        for state in rr.states:
            if state[0] == 1:
                print(state)
                sidx = rr.states.index(state)
                if state in policy:
                    print("\nState: ", state)
                    print("Q: ", Q[sidx])
                    print("Policy: ", rr.action_names[policy[state]])
                input() 
        """ 





if __name__ == "__main__":
    logging.basicConfig(filename="run_experiment.log", filemode="w", format='%(asctime)s %(message)s', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(console)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    logging.info("----------- Start of new experiment. -----------")

    main()