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
        "p": 1/3,
        "nom_sev_probs": ["0.1", "0.15", "0.2", "0.25", "0.3"],
    },

    "L": {
        "type": "forbidden",
        "p": 1/3,
        "nom_sev_probs": ["0.25", "0.25", "0.2", "0.2", "0.1"],
    },

    "P": {
        "type": "forbidden",
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


severity_probs = np.array([float(Fraction(i)) for i in self.environment_info[terrain]["nom_sev_probs"]])