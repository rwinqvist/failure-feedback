import numpy as np 
import logging 
from rocky_road import RockyRoad
from env_wrapper import EnvironmentWrapper
from solvers import ValueIteration



MAPS = {
    "3x5": ["RRPRP", "SAAAG", "RRPRR"],
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 3,
    "action_costs": [1, 3, 6],
    "nom_success_rate": 0.65,
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 200,

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
        "p": 1/3,
        #"nom_sev_probs": [0.1, 0.15, 0.2, 0.25, 0.3],
        "nom_sev_probs": [0.2, 0.2, 0.2, 0.2, 0.2],
    },

    "L": {
        "type": "forbidden",
        "p": 1/3,
        "nom_sev_probs": [0.25, 0.25, 0.2, 0.2, 0.1],
        #"nom_sev_probs": [0.2, 0.2, 0.2, 0.2, 0.2],
        #"nom_sev_probs": [0.1, 0.15, 0.2, 0.25, 0.3],
    },

    "P": {
        "type": "forbidden",
        "p": 1/3,
        #"nom_sev_probs": [0.2, 0.2, 0.2, 0.2, 0.2],
        "nom_sev_probs": [0.1, 0.15, 0.2, 0.25, 0.3],
    }
}


EXP_INFO = {
    "max_acc_sev": 50,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}


def check_T_rr(rr):
    for (sidx, state) in enumerate(rr.states):
        for action in rr.actions: 
            print("\nState: ", state)
            print("Action: ", action)
            next_sidxs = np.where(rr.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = rr.states[next_sidx]
                print("Next: ", next_state, "p: ", rr.T[sidx, action, next_sidx])
                
            T_sum = sum(rr.T[sidx, action])
            if T_sum != 1:
                print("WARNING! T sums to: ", T_sum)
            input()

def check_R_rr(rr):
    for (sidx, state) in enumerate(rr.states):
        for action in rr.actions: 
            print("\nState: ", state)
            print("Action: ", action)
            next_sidxs = np.where(rr.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = rr.states[next_sidx]
                print("Next: ", next_state, "p: ", rr.T[sidx, action, next_sidx], "r: ", rr.R[sidx, action, next_sidx])
                
            T_sum = sum(rr.T[sidx, action])
            if T_sum != 1:
                print("WARNING! T sums to: ", T_sum)
            input()

def check_severity_maps_rr(rr):
    for key, item in rr.severity_map.items():
        print(key, item)

    for (sidx, state) in enumerate(rr.states):
        if state not in rr.goal_states and state not in rr.bouncing_states:
            for action in rr.actions: 
                next_sidxs = np.where(rr.T[sidx, action] != 0)[0]
                for next_sidx in next_sidxs: 
                    next_state = rr.states[next_sidx]
                    print("\n\nState: ", state)
                    print("Action: ", action)
                    print("Next: ", next_state)
                    if next_state in rr.bouncing_states:
                        sev_probs = rr.T_sev[sidx, action, next_sidx]
                        print("sev probs: ", sev_probs)
                    input()

def check_faliure_transitions_rr(rr): 
    for (sidx, state) in enumerate(rr.states):
        if state not in rr.goal_states and state not in rr.bouncing_states:
            for action in rr.actions: 
                print("\n\nState: ", state)
                print("Action: ", action)
                print("Failure transitions: ", rr.failure_transitions[state][action])
                input()


def check_T_ew(env):
    for (sidx, state) in enumerate(env.states):
        for action in env.actions: 
            print("\nState: ", state)
            print("Action: ", action)
            next_sidxs = np.where(env.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = env.states[next_sidx]
                print("Next: ", next_state, "p: ", env.T[sidx, action, next_sidx])
                
            T_sum = sum(env.T[sidx, action])
            if T_sum != 1:
                print("WARNING! T sums to: ", T_sum)
            input()

def check_R_ew(env):
    for (sidx, state) in enumerate(env.states):
        for action in env.actions: 
            print("\nState: ", state)
            print("Action: ", action)
            next_sidxs = np.where(env.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = env.states[next_sidx]
                print("Next: ", next_state, "p: ", env.T[sidx, action, next_sidx], "r: ", env.R[sidx, action, next_sidx])
                
            T_sum = sum(env.T[sidx, action])
            if T_sum != 1:
                print("WARNING! T sums to: ", T_sum)
                input()


def check_O_ew(env):
    for (sidx, state) in enumerate(env.states):
        for action in env.actions: 
            print("\nState: ", state)
            print("Action: ", action)
            next_sidxs = np.where(env.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = env.states[next_sidx]
                print("Next: ", next_state, "p: ", env.T[sidx, action, next_sidx], "r: ", env.R[sidx, action, next_sidx], "o: ", env.O[sidx, action, next_sidx])
                
            T_sum = sum(env.T[sidx, action])
            if T_sum != 1:
                print("WARNING! T sums to: ", T_sum)
            input()


def check_policy(env, policy, Q):
    for (sidx, state) in enumerate(env.states):
        if state in policy:
            action = policy[state]
            if action == 1:
                print("\nState: ", state)
                print("Policy: ", policy[state])
                print("Q: ", Q[sidx])
                input()


def main(): 
    env_info = ENV_INFO
    exp_info = EXP_INFO
    #map = MAPS["3x5"]
    rr = RockyRoad(env_info)
    print("Map: \n", rr.map, "\n")

    #check_T_rr(rr)
    #check_R_rr(rr)
    #check_severity_maps_rr(rr)
    #check_faliure_transitions_rr(rr)

    env = EnvironmentWrapper(rr, exp_info)    
    #check_T_ew(env)
    #check_R_ew(env)
    #check_O_ew(env)

    alg = ValueIteration(env)
    V, Q, policy = alg.run()
    check_policy(env, policy, Q)



    


if __name__ == "__main__":
    main()