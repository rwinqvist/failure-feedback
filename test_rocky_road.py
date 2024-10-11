import numpy as np 
import logging 
from rocky_road import RockyRoad
from env_wrapper import EnvironmentWrapper
from solvers import ValueIteration
from mcdomp_planner import MCOMDP_Planner



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
    "true_obs_prob": 0.4,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": [1, 3, 6, 10, 15],
    "action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 400,

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
    "max_acc_sev": 18,
    "query_cost": 1,
    "severity_penalty_weight": 2,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 400,

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
    "max_acc_sev": 18,
    "query_cost": 1,
    "severity_penalty_weight": 2,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 300,

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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}



ENV_INFO =  {   
    "length": 40,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 2,
    "goal_reward": 400,

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
    "max_acc_sev": 60,
    "query_cost": 1,
    "severity_penalty_weight": 8,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 300,

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
        #"nom_sev_probs": [0.2, 0.2, 0.2, 0.2, 0.2],
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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.25,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 300,

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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 700,

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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
}



#####################################
#####################################
#####################################

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": list(0.5*np.array([1.0, 2.0, 4.0, 8.0, 16.0])),
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.8,
    "severity_decline_factor": 1,
    "skew_factor": 1,
    "goal_reward": 250,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 0.2,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 1,
    "skew_factor": 1,
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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 2*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 1,
    "skew_factor": 2,
    "goal_reward": 1200,

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
    "max_acc_sev": 15,
    "query_cost": 1,
    "severity_penalty_weight": 10,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.85,
    "skew_factor": 1,
    "goal_reward": 1700,

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
    "max_acc_sev": 40,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.3, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 0.75,
    "skew_factor": 1,
    "goal_reward": 500,

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
    "true_obs_prob": 0.1,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.925,
    "skew_factor": 1,
    "goal_reward": 500,

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
    "max_acc_sev": 20,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 2000,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": list(0.5*np.array([1, 2, 4, 8, 16])),
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.95, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.6, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 2000,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



MAP = ['LPLLPPPRPLPPPRPPRLPR', 'SAAAAAAAAAAAAAAAAAAG', 'LPRRLRRPLRPRRLRRLLRL']
MAP = ['PRLLLRLRRLLLRLPPRPPR', 'SAAAAAAAAAAAAAAAAAAG', 'LRLLLLRRPLLLRLPRPPPR']


ENV_INFO =  {   
    "length": 10,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 600,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 0.25,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 500,

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
    "max_acc_sev": 35,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.9,
    "skew_factor": 1.5,
    "goal_reward": 400,

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
    "max_acc_sev": 35,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    "action_costs": 1*[1, 2, 4, 8, 16],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 600,

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
    "max_acc_sev": 40,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.85, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 600,

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
    "max_acc_sev": 40,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[1, 2, 4, 8, 16, 32],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.9,
    "skew_factor": 1.5,
    "goal_reward": 400,

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
    "max_acc_sev": 35,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 50,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.8,
    "skew_factor": 1,
    "goal_reward": 10000,

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
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.8,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 500,

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
    "max_acc_sev": 22,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 15,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.8,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 2000,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "goal_reward": 5000,

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
    "max_acc_sev": 30,
    "query_cost": 1,
    "severity_penalty_weight": 10,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 40,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 3000,

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
    "max_acc_sev": 20,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 40,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 10, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 10000,

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
    "max_acc_sev": 30,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.5, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.95,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 3000,

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
    "true_obs_prob": 0.1,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.65, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "goal_reward": 2000,

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
    "max_acc_sev": 30,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
    "alpha": 0.35,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.7, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.9,
    "severity_decline_factor": 0.6,
    "skew_factor": 1,
    "goal_reward": 2000,

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
    "max_acc_sev": 28,
    "query_cost": 1,
    "severity_penalty_weight": 15,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
    "alpha": 1,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.78, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "severity_decline_factor": 0.6,
    "skew_factor": 1,
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
    "max_acc_sev": 28,
    "query_cost": 1,
    "severity_penalty_weight": 10,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
    "alpha": 0.85,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.78, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
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
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "max_acc_sev": 28,
    "query_cost": 1,
    "severity_penalty_weight": 10,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.78, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.8,
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
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "max_acc_sev": 28,
    "query_cost": 1,
    "severity_penalty_weight": 15,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.78, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 500,

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
    "severity_decline_factor": 0.9,
    "skew_factor": 1,
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 20,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}


ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 700,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}

ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 500,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 25,
    "recovery_rate": 0,
    "true_obs_prob": 0.2,
    "alpha": 0.85,
}



ENV_INFO =  {   
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.75, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.85,
    "goal_reward": 800,

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
    "max_acc_sev": 25,
    "query_cost": 1,
    "severity_penalty_weight": 20,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
    "alpha": 0.85,
}


ENV_INFO =  {   
    "length": 40,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": 1*[2, 4, 8, 16, 32],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.6, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.8,
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
    "max_acc_sev": 30,
    "query_cost": 1,
    "severity_penalty_weight": 40,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
}




MAP = None
MAP = ['LLPPLLPRRLRRPPPRPLPL', 'SAAAAAAAAAAAAAAAAAAG', 'PPRPRLLRRLPPPLRRPLPR']
map = ['PRRRPPRRPRLLPLLPRRLR', 'SAAAAAAAAAAAAAAAAAAG', 'PPPPLPRRRPLPLLLRRRRP']
MAP = ['PRRRPPRRPRLLPLLPRRLR', 'SAAAAAAAAAAAAAAAAAAG', 'PPPPLPRRRPLPLLLRRRRP']
MAP = None

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
            if not np.isclose(T_sum, 1):
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
            #print("\nState: ", state)
            #print("Action: ", action)
            #print("T: ", env.T[sidx, action])
            #input()
            next_sidxs = np.where(env.T[sidx, action] != 0)[0]
            for next_sidx in next_sidxs:
                next_state = env.states[next_sidx]
                #print("Next: ", next_state, "p: ", env.T[sidx, action, next_sidx])
                #input()
            T_sum = sum(env.T[sidx, action])
            if not np.isclose(T_sum, 1):
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
            #if action == 1:
            print("\nState: ", state)
            print("Policy: ", action)
            print("Q: ", Q[sidx])
            input()


def main(): 
    env_info = ENV_INFO
    exp_info = EXP_INFO
    #map = MAPS["3x5"]
    map = None
    rr = RockyRoad(env_info, map=map)
    print(rr.board)
    for key, item in rr.action_info.items():
        print(key, item)
    #input()
    #print("Map: \n", rr.map, "\n")

    #check_T_rr(rr)
    #check_R_rr(rr)
    #check_severity_maps_rr(rr)
    #check_faliure_transitions_rr(rr)

    env = EnvironmentWrapper(rr, exp_info)    
    check_T_ew(env)
    #check_R_ew(env)
    #check_O_ew(env)

    alg = ValueIteration(env)
    print("VI solvingz")
    V, Q, policy = alg.run()
    #check_policy(env, policy, Q)
    
    env.set_QMDP(Q)
    env.set_VMDP(V) 

    planner = MCOMDP_Planner(env, exp_info)
    num_episodes = 1
    rewards, severities, step_count, query_count, failure_count, query_states, query_beliefs = planner.run(num_episodes)


    


if __name__ == "__main__":
    main()