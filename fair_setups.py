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
    "goal_reward": 50,

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
    "length": 20,
    "terrains": ["A", "C", "R", "L", "P"],
    "severity_levels": [1, 2, 3, 4, 5],
    "num_actions": 5,
    #"action_costs": 1*[1, 2, 4, 8, 16],
    "action_costs": list(1*np.array([2, 4, 8, 16, 32])),
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.75,
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
    "max_acc_sev": 10,
    "query_cost": 10,
    "severity_penalty_weight": 5,
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
    #"action_costs": list(0.1*np.array([2, 4, 8, 16, 32])),
    "action_costs": [1, 2, 3, 4, 5],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.9, #0.9 good, #0.8 pretty good too
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
}


EXP_INFO = {
    "severity_decline_factor": 0.95,
    "skew_factor": 1,
    "max_acc_sev": 10,
    "query_cost": 1,
    "severity_penalty_weight": 0,
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
    #"action_costs": list(0.1*np.array([2, 4, 8, 16, 32])),
    "action_costs": [1,2,3,4,5],
    #"action_costs": 2*[1, 2, 3, 4, 5],
    #"action_costs": [1, 3, 6, 105, 15],
    #"action_costs": [3, 7, 12, 18, 25],
    "nom_success_rate": 0.8, #0.9 good, #0.8 pretty good too
    "risky_decline_factor": 0.90,
    "goal_reward": 175,

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
    "max_acc_sev": 10,
    "query_cost": 1,
    "severity_penalty_weight": 1,
    "recovery_rate": 0,
    "true_obs_prob": 0.1,
    "alpha": 0.85,
}


