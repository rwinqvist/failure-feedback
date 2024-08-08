import numpy as np 
import logging
import json 
import jsbeautifier
from datetime import datetime
from rocky_road import RockyRoad
from mdp_solvers import ValueIteration
from environment_wrapper import EnvironmentWrapper
from mcomdp_planner import MCOMDP_Planner
from py_setup import env_data 
from py_setup import exp_data


TEST = 0 
SIM = 1


ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severities": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "nom_success_rate": 0.6,
    "action_cost_increment": 1,
    "risky_decline_factor": 0.7,
    "severity_decline_factor": 0.8,
    "skew_factor": 2,
    "goal_reward": 1000,

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
        "nom_sev_probs": [0.1, 0.15, 0.2, 0.25, 0.3],
    },

    "L": {
        "type": "forbidden",
        "p": 1/3,
        "nom_sev_probs": [0.25, 0.25, 0.2, 0.2, 0.1],
    },

    "P": {
        "type": "forbidden",
        "p": 1/3,
        "nom_sev_probs": [0.2, 0.2, 0.2, 0.2, 0.2],
    }
}

EXP_INFO = { 
    "true_obs_prob": 0.1,
    "query_cost": 1,
    "severity_penalty_weight": 0,
    "recovery_rate": 0.5,
    "halt_factor": 1.2
}


def main_tests():
    num_runs = 1
    num_episodes = 5

    #env_num = 1 
    #env_name = f"env{env_num}"
    #exp_num = 1 
    #exp_name = f"exp{exp_num}"

    env_info = ENV_INFO
    exp_info = EXP_INFO
    env_name = "custom"
    exp_name = "custom"

    for i in range(num_runs):
        #env_info = env_data.ENV_INFO[env_name]
        #exp_info = exp_data.EXP_INFO[exp_name]

        rr = RockyRoad(env_info, use_preset_map=False, is_uneven=True)
        rr.print_action_info()

        alg = ValueIteration(rr)
        V, Q, policy = alg.run()
    
        env = EnvironmentWrapper(environment=rr, experiment_info=exp_info, )

        alg = ValueIteration(env)
        V, Q, policy = alg.run()

        env.set_VMDP(V)
        env.set_QMDP(Q)

        planner = MCOMDP_Planner(env, exp_info)
        rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs = planner.run(num_episodes)

        sim_info = get_sim_info(num_episodes, rr.map)
        env_info_data = get_env_info(env_info, env_name)
        exp_info_data = get_exp_info(exp_info, exp_name)
        results = get_results(rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs)

        type = TEST
        save_data(type, sim_info, env_info_data, exp_info_data, results)



def main():
    num_runs = 1
    num_episodes = 1

    env_num = 1 
    env_name = f"env{env_num}"
    exp_num = 1 
    exp_name = f"exp{exp_num}"

    for i in range(num_runs):
        env_info = env_data.ENV_INFO[env_name]
        exp_info = exp_data.EXP_INFO[exp_name]

        rr = RockyRoad(env_info, use_preset_map=False, is_uneven=True)
        print("Map: \n", rr.map, "\n\n")
        rr.print_action_info()

        alg = ValueIteration(rr)
        V, Q, policy = alg.run()

    
        env = EnvironmentWrapper(environment=rr, experiment_info=exp_info, )

        alg = ValueIteration(env)
        V, Q, policy = alg.run()

        env.set_VMDP(V)
        env.set_QMDP(Q)

        planner = MCOMDP_Planner(env, exp_info)
        rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs = planner.run(num_episodes)


        sim_info = get_sim_info(num_episodes)
        env_info_data = get_env_info(env_info, env_name)
        exp_info_data = get_exp_info(exp_info, exp_name)
        results = get_results(rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs)

        type = SIM
        save_data(type, sim_info, env_info_data, exp_info_data, results)


def get_sim_info(num_episodes, map):
    list_map = map.flatten().tolist()
    list_map = [str(bytes(byte_str).decode()) for byte_str in list_map]

    data = {
        "num_episodes": num_episodes,
        "map": list_map
    }
    
    return data

def get_env_info(env_info, env_name):
    data = env_info 
    data["name"] = env_name
    return data

def get_exp_info(exp_info, exp_name):
    data = exp_info 
    data["name"] = exp_name
    return data

def get_results(rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs):
    query_rates = np.array(query_count)/np.array(failure_count)
    data = {
        "rewards": rewards.tolist(), 
        "severities": severities.tolist(),
        "steps": step_count.tolist(),
        "queries": query_count.tolist(),
        "failures": failure_count.tolist(),
        "query_rates": query_rates.tolist(),
        "query_states": query_states, 
        "query_beliefs": query_beliefs
    }

    return data


def save_data(type, sim_info, env_info, exp_info, results):
    if type == TEST:
        path = "test_runs/"
        name = "test"

    elif type == SIM:
        path = "simulation_data/"
        name = today = datetime.today().strftime('%Y-%m-%d')

    fn = "info.json"
    with open(path+fn, "r") as info_file:
        info = json.load(info_file)
    
    if name in info: 
        sim_num = info[name] + 1
    else: 
        sim_num = 1

    info[name] = sim_num

    with open(path+fn, "w") as info_file:
        json.dump(info, info_file)

    filename = f"{name}_{sim_num}"
    data = {
        "sim_info" : sim_info,
        "env_info": env_info,
        "exp_info": exp_info,
        "results" : results
    }

    options = jsbeautifier.default_options()
    options.indent_size = 4
    json_obj = jsbeautifier.beautify(json.dumps(data), options)

    with open(path+filename+".json", "w") as json_file:
        json.dump(data, json_file)

    with open(path+filename+".txt", "w") as txt_file: 
        txt_file.write(json_obj)




if __name__ == "__main__":
    logging.basicConfig(filename="run_experiment.log", filemode="w", format='%(asctime)s %(message)s', level=logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    
    logging.info("----------- Start of new experiment. -----------")

    #main()
    main_tests()


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