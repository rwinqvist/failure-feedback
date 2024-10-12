import numpy as np
import logging 
import matplotlib.pyplot as plt
import math
import json 
import jsbeautifier
from rocky_road import RockyRoad, generate_random_road_map
from solvers import ValueIteration
from env_wrapper import EnvironmentWrapper
from mcdomp_planner import MCOMDP_Planner
from setups import SETUPS

ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 0,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


################################################
################################################
ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 2,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}

################################################
################################################

ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    #"action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}







###### started here when testing again
ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}




ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.6,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}

ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 3,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    #"action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "action_costs": [1,2,3,4,5],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 100,

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
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 15,
    "query_cost": 3,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


INFO =  {"ENV_INFO":
            {   
                "length": 20,
                "terrains": ["A", "C", "R", "L", "P"],
                "severity_levels": [1, 2, 3, 4, 5],
                "num_actions": 5,
                #"action_costs": 1*[1, 2, 4, 8, 16],
                #"action_costs": list(0.1*np.array([2, 4, 8, 16, 32])),
                "action_costs": [1, 2, 3, 4, 5],
                #"action_costs": 2*[1, 2, 3, 4, 5],
                #"action_costs": [1, 3, 6, 105, 15],
                #"action_costs": [3, 7, 12, 18, 25],
                "nom_success_rate": 0.9,  #0.9 good, #0.8 pretty good too
                "risky_decline_factor": 0.9,
                "goal_reward": 100,

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
            },
            "EXP_INFO": 
            {
                "severity_decline_factor": 0.95,
                "skew_factor": 1,
                "max_acc_sev": 40,
                "query_cost": 1,
                "severity_penalty_weight": 1,
                "recovery_rate": 0,
                "true_obs_prob": 0.1,
                "alpha": 0.85,
            }
        }






def main():
    num_maps = 10
    num_episodes = 200
    heuristics = ["always", "alg", "never"]
    

    #map = ['PLLLRLPLPLPRPLRRPRPPLPPPRRRPRLLRLLLRLPPR', 'SAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG', 'PPPRLLPLPPPLLLRRRLRPLRPLLLRLPLPPPLLRPLPR']
    bests = []
    for i in range(num_maps):
        print("\n\n---------------- NEW RUN: ", i+1, " ----------------")
        env_info = ENV_INFO
        exp_info = EXP_INFO

        rr = RockyRoad(env_info)
        env = EnvironmentWrapper(environment=rr, exp_info=exp_info)
        alg = ValueIteration(env)
        V, Q, policy = alg.run()
        env.set_QMDP(Q)
        env.set_VMDP(V)

        best = None
        rate = -math.inf
        for heuristic in heuristics:
            #print("\nheuristic: ", heuristic)
            r = 0
            planner = MCOMDP_Planner(env, exp_info, query_heuristic=heuristic)
            rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs = planner.run(num_episodes)

            avg_rewards = []
            query_rate = []
            for i in range(num_episodes):
                avg_rewards.append(rewards[i]/step_count[i])
                if failure_count[i] != 0:
                    query_rate.append(query_count[i]/failure_count[i])
                else:
                    query_rate.append(0)
                #failure_rate = failure_count[i]/step_count[i]
                #if failure_rate != 0:
                    #print("avg reward: ", rewards[i]/failure_rate)
                    #avg_rewards.append(rewards[i]/failure_rate)

            avg = sum(avg_rewards)/len(avg_rewards)
            if avg > rate:
                best = heuristic
                rate = avg
            #print("avg over all episodes: ", avg)
            #print("query rates: ", query_rate)
        bests.append(best)
    
    print("alg count: ", bests.count("alg")/len(bests))
    print("never count: ", bests.count("never")/len(bests))
    print("always count: ", bests.count("always")/len(bests))



def unpack_env_info(env_info):
    forbidden_terrains_info = {}
    allowed_terrains_info = {}

    terrain_types = env_info["terrains"]
    for terrain in terrain_types:
        if env_info[terrain]["type"] == "forbidden":
            forbidden_terrains_info[terrain] = env_info[terrain]["p"]

        elif env_info[terrain]["type"] == "allowed":
            allowed_terrains_info[terrain] = env_info[terrain]["p"]

    return allowed_terrains_info, forbidden_terrains_info


def mc_comparison(env, exp, num_maps, num_episodes, heuristics=["alg", "always", "never"]):
    """
    Num runs can be interpreted as number of different maps...
    Num episodes is how many times each map is simulated for each query heuristic
    """

    env_info = env
    exp_info = exp
    length = env_info["length"]
    allowed_terrains_info, forbidden_terrains_info = unpack_env_info(env_info)

    simulated_maps = []
    
    all_data = {heuristic: {} for heuristic in heuristics}

    for i in range(num_maps):
        # need to ensure we're not simulating an already simulated map 
        print(f"\nRun: {i+1}")
        _, map = generate_random_road_map(length, allowed_terrains_info, forbidden_terrains_info)
        while map in simulated_maps:
            map = generate_random_road_map(length, allowed_terrains_info, forbidden_terrains_info)
        simulated_maps.append(map)

        rr = RockyRoad(env_info, map=map)
        env = EnvironmentWrapper(environment=rr, exp_info=exp_info)
        alg = ValueIteration(env)
        V, Q, policy = alg.run() 
        env.set_QMDP(Q)
        env.set_VMDP(V)


        for heuristic in heuristics:
            #print("Heuristic: ", heuristic)
            data = {"rewards": [], "step_count": [], "query_count": [], "failure_count": []}
            episode = 0

            while episode < num_episodes:
                #print("Episode: ", episode)
                planner = MCOMDP_Planner(env, exp_info, query_heuristic=heuristic)
                rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs = planner.run(1)
                #print("query rate: ", np.count_nonzero(query_count[0]/failure_count[0]))
                #time.sleep(0.2)

                if 0 not in failure_count:
                    episode += 1 
                    data["rewards"].append(rewards[0]) 
                    data["step_count"].append(step_count[0])
                    data["failure_count"].append(failure_count[0])
                    data["query_count"].append(query_count[0])

            all_data[heuristic][i] = data 

    return all_data
    plot_reward_vs_failure_rate(num_maps, all_data, heuristics, block=True, subplot=False)
    #boxplot(num_maps, all_data, heuristics, block=False)
    #shaded_plot(num_maps, all_data, heuristics)


def boxplot(num_maps, all_data, heuristics, block):
    fig = plt.figure(figsize=(8,12))
    ax_fr = fig.add_subplot(121)
    ax_sc = fig.add_subplot(122)
    ax_fr.set_ylabel('Relative reward (FR)')
    ax_fr.set_xlabel('Map num')
    ax_sc.set_ylabel('Relative reward (SC)')
    ax_sc.set_xlabel('Map num')

    for heuristic in heuristics:
        xs, ys_fr, ys_sc = [], [], []
        q1_fr, q3_fr, q1_sc, q3_sc = [], [], [], []

        data = all_data[heuristic]
        for i in range(num_maps):
            rewards = data[i]["rewards"]
            failure_count = data[i]["failure_count"]
            step_count = data[i]["step_count"]
            failure_rate = np.array(failure_count)/np.array(step_count)

            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)

            xs.append(i)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))

            q1_fr.append(np.percentile(rel_reward_fr, 10)) 
            q3_fr.append(np.percentile(rel_reward_fr, 90)) 
            q1_sc.append(np.percentile(rel_reward_sc, 10)) 
            q3_sc.append(np.percentile(rel_reward_sc, 90)) 

            #rel_reward = np.array(rewards)/failure_rate 

        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        q1_fr, q3_fr, q1_sc, q3_sc = np.array(q1_fr), np.array(q3_fr), np.array(q1_sc), np.array(q3_sc)
        ax_fr.errorbar(xs, ys_fr, yerr=[ys_fr - q1_fr, q3_fr - ys_fr], capsize=10)
        ax_sc.errorbar(xs, ys_sc, yerr=[ys_sc - q1_sc, q3_sc - ys_sc], capsize=10)

    plt.legend(heuristics)
    plt.show(block=block)


def shaded_plot_old(num_maps, all_data, heuristics):
    fig = plt.figure(figsize=(8,12))
    ax_fr = fig.add_subplot(121)
    ax_sc = fig.add_subplot(122)
    ax_fr.set_ylabel('Relative reward (FR)')
    ax_fr.set_xlabel('Map num')
    ax_sc.set_ylabel('Relative reward (SC)')
    ax_sc.set_xlabel('Map num')

    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas = [0.5, 0.3, 0.1]

    for (hix, heuristic) in enumerate(heuristics):
        xs, ys_fr, ys_sc = [], [], []
        std_fr, std_sc = [], []

        data = all_data[heuristic]
        for i in range(num_maps):
            rewards = data[i]["rewards"]
            failure_count = data[i]["failure_count"]
            step_count = data[i]["step_count"]
            failure_rate = np.array(failure_count)/np.array(step_count)

            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)

            xs.append(i)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))

            std_fr.append(np.std(rel_reward_fr)) 
            std_sc.append(np.std(rel_reward_sc)) 

            #rel_reward = np.array(rewards)/failure_rate 

        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        
        c = default_colors[hix]
        a = alphas[hix]
        ax_fr.plot(xs, ys_fr, color=c)
        ax_fr.fill_between(xs, ys_fr - std_fr, ys_fr + std_fr, color=c, alpha=a)
        ax_sc.plot(xs, ys_sc, color=c)
        ax_sc.fill_between(xs, ys_sc - std_sc, ys_sc + std_sc, color=c, alpha=a)

    plt.legend(heuristics)
    plt.show()
            

def plot_reward_vs_failure_rate(num_maps, all_data, heuristics, block, subplot=True):
    fig = plt.figure(figsize=(8,12))
    if subplot:
        ax_fr = fig.add_subplot(121)
        ax_sc = fig.add_subplot(122)
        ax_fr.set_ylabel('Relative reward (FR)')
        ax_fr.set_xlabel('Map num')
        ax_sc.set_ylabel('Relative reward (SC)')
        ax_sc.set_xlabel('Map num')

    else:
        ax = fig.add_subplot(111)
        ax.set_ylabel('Relative reward')
        ax.set_xlabel('Map num')

    for heuristic in heuristics:
        xs, ys_fr, ys_sc = [], [], []
        data = all_data[heuristic]
        for i in range(num_maps):
            # avg results over all episodes 
            rewards = data[i]["rewards"]
            step_count = data[i]["step_count"]
            failure_count = data[i]["failure_count"]
            query_count = data[i]["query_count"]

            failure_rate = np.array(failure_count)/np.array(step_count)
            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)
            xs.append(i)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))

        if subplot:
            ax_fr.plot(list(xs), list(ys_fr), '-o', label=f"{heuristic}")
            ax_sc.plot(list(xs), list(ys_sc), '-o', label=f"{heuristic}")

        else:
            ax.plot(list(xs), list(ys_sc), '-o', label=f"{heuristic}")
        #continue
        #plt.show()
        
    plt.legend()
    plt.show(block=block)
        


def mean_plot(num_maps, all_data, heuristics, fn, block=True):
    fig1, fig2 = plt.figure(figsize=(8,12)), plt.figure(figsize=(8,12))
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)

    ax_fr.set_ylabel('Relative reward (FR)')
    ax_fr.set_xlabel('Map num')
    ax_sc.set_ylabel('Relative reward (SC)')
    ax_sc.set_xlabel('Map num')

    for heuristic in heuristics:
        xs, ys_sc, ys_fr = [], [], []
        data = all_data[heuristic]
        for map in range(num_maps):
            rewards = data[map]["rewards"]
            step_count = data[map]["step_count"]
            failure_count = data[map]["failure_count"]
            query_count = data[map]["query_count"]

            failure_rate = np.array(failure_count)/np.array(step_count)
            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)

            xs.append(map)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))
        
        ax_fr.plot(list(xs), list(ys_fr), '-o', label=f"{heuristic}")
        ax_sc.plot(list(xs), list(ys_sc), '-o', label=f"{heuristic}")


    fig1.legend() 
    fig2.legend()

    #plt.show(block=block)

    # Save figure 
    fig1.savefig(fn+"_mean_sc.png")
    fig2.savefig(fn+"_mean_fr.png")
    

def box_plot(num_maps, all_data, heuristics, fn, block=True):
    fig1, fig2 = plt.figure(figsize=(8,12)), plt.figure(figsize=(8,12))
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)

    ax_fr.set_ylabel('Relative reward (FR)')
    ax_fr.set_xlabel('Map num')
    ax_sc.set_ylabel('Relative reward (SC)')
    ax_sc.set_xlabel('Map num')

    for heuristic in heuristics:
        xs, ys_fr, ys_sc = [], [], []
        q1_fr, q3_fr, q1_sc, q3_sc = [], [], [], []

        data = all_data[heuristic]
        for i in range(num_maps):
            rewards = data[i]["rewards"]
            failure_count = data[i]["failure_count"]
            step_count = data[i]["step_count"]
            failure_rate = np.array(failure_count)/np.array(step_count)

            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)

            xs.append(i)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))

            q1_fr.append(np.percentile(rel_reward_fr, 25)) 
            q3_fr.append(np.percentile(rel_reward_fr, 75)) 
            q1_sc.append(np.percentile(rel_reward_sc, 25)) 
            q3_sc.append(np.percentile(rel_reward_sc, 75)) 

            #rel_reward = np.array(rewards)/failure_rate 

        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        q1_fr, q3_fr, q1_sc, q3_sc = np.array(q1_fr), np.array(q3_fr), np.array(q1_sc), np.array(q3_sc)
        ax_fr.errorbar(xs, ys_fr, yerr=[ys_fr - q1_fr, q3_fr - ys_fr], capsize=10)
        ax_sc.errorbar(xs, ys_sc, yerr=[ys_sc - q1_sc, q3_sc - ys_sc], capsize=10)

    
    fig1.legend(heuristics) 
    fig2.legend(heuristics)

    #plt.show(block=block)

    # Save figure 
    fig1.savefig(fn+"_box_sc.png")
    fig2.savefig(fn+"_box_fr.png")



def shaded_plot(num_maps, all_data, heuristics, fn, block=True):
    fig1, fig2 = plt.figure(figsize=(8,12)), plt.figure(figsize=(8,12))
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)

    ax_fr.set_ylabel('Relative reward (FR)')
    ax_fr.set_xlabel('Map num')
    ax_sc.set_ylabel('Relative reward (SC)')
    ax_sc.set_xlabel('Map num')

    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas = [0.2, 0.2, 0.2]

    for (hix, heuristic) in enumerate(heuristics):
        xs, ys_fr, ys_sc = [], [], []
        std_fr, std_sc = [], []

        data = all_data[heuristic]
        for i in range(num_maps):
            rewards = data[i]["rewards"]
            failure_count = data[i]["failure_count"]
            step_count = data[i]["step_count"]
            failure_rate = np.array(failure_count)/np.array(step_count)

            rel_reward_fr = np.array(rewards)/failure_rate
            rel_reward_sc = np.array(rewards)/np.array(step_count)

            xs.append(i)
            ys_fr.append(np.mean(rel_reward_fr))
            ys_sc.append(np.mean(rel_reward_sc))

            std_fr.append(np.std(rel_reward_fr)) 
            std_sc.append(np.std(rel_reward_sc)) 


        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        
        c = default_colors[hix]
        a = alphas[hix]
        ax_fr.plot(xs, ys_fr, color=c)
        ax_fr.fill_between(xs, ys_fr - std_fr, ys_fr + std_fr, color=c, alpha=a)
        ax_sc.plot(xs, ys_sc, color=c)
        ax_sc.fill_between(xs, ys_sc - std_sc, ys_sc + std_sc, color=c, alpha=a)


    fig1.legend(heuristics) 
    fig2.legend(heuristics)

    #plt.show(block=block)

    # Save figure 
    fig1.savefig(fn+"_shaded_sc.png")
    fig2.savefig(fn+"_shaded_fr.png")


def plot_data(setup, all_data, heuristics, block, env="rocky_road"):
    path = f"exp_data/{env}/"
    env, exp, num_maps, num_sims = setup["env"], setup["exp"], setup["num_maps"], setup["num_sims"]
    fn = f"{env}_{exp}_{num_maps}maps_{num_sims}sims"

    mean_plot(num_maps, all_data, heuristics, path+fn, block=False)
    box_plot(num_maps, all_data, heuristics, path+fn, block=False) 
    shaded_plot(num_maps, all_data, heuristics, path+fn, block=False)



def save_data(setup, all_data, heuristics, env="rocky_road"):
    path = f"exp_data/{env}/"
    env, exp, num_maps, num_sims = setup["env"], setup["exp"], setup["num_maps"], setup["num_sims"]
    fn = f"{env}_{exp}_{num_maps}maps_{num_sims}sims"

    # structure data for json file 
    data = {"env": env,
            "exp": exp,
            "num_maps": num_maps, 
            "num_sims": num_sims} 
    
    for heuristic in heuristics:
        data[heuristic] = all_data[heuristic]


    options = jsbeautifier.default_options() 
    options.indent_size = 4 
    json_obj = jsbeautifier.beautify(json.dumps(data), options)

    with open(path+fn+".json", "w") as json_file:
        json.dump(data, json_file)

    with open(path+fn+".txt", "w") as txt_file:
        txt_file.write(json_obj)



if __name__ == "__main__":
    #logging.basicConfig(filename="run_experiment.log", filemode="w", format='%(asctime)s %(message)s', level=logging.DEBUG)
    #console = logging.StreamHandler()
    #console.setLevel(logging.INFO)
    #logging.getLogger('').addHandler(console)
    #logging.getLogger('matplotlib').setLevel(logging.WARNING)
    #
    #logging.info("----------- Start of new experiment. -----------")

    env = "ENV20_2"
    exp = "EXP20_2"
    num_maps = 50
    num_sims = 500
    setup = {"env": env, 
             "exp": exp,
             "num_maps": num_maps, 
             "num_sims": num_sims}
    
    heuristics = ["alg", "always", "never"]

    all_data = mc_comparison(SETUPS[env], SETUPS[exp], num_maps, num_sims, heuristics=heuristics)
    plot_data(setup, all_data, heuristics, block=True)
    save_data(setup, all_data, heuristics)
    #main()





