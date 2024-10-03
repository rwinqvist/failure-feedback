import numpy as np 
import logging 
from fractions import Fraction 

# ACTIONS 
RIGHT = 0

ROAD_MAPS = {}

UP = "up"
DOWN = "down"


def generate_random_road_map(length, allowed_terrains_info, forbidden_terrains_info, seed=None):
    logging.info("Generating road map...")
    board = [] 

    allowed_terrains = list(allowed_terrains_info.keys())
    allowed_probs = list(allowed_terrains_info.values())

    forbidden_terrains = list(forbidden_terrains_info.keys())
    forbidden_probs = list(forbidden_terrains_info.values())

    np.random.seed(seed)
    r1 = np.random.choice(forbidden_terrains, (1, length), p=forbidden_probs)
    r2 = np.random.choice(allowed_terrains, (1, length), p=allowed_probs)
    r3 = np.random.choice(forbidden_terrains, (1, length), p=forbidden_probs)

    board = np.vstack((r1, r2, r3))

    board[1][0] = "S"           # start tile middle far left
    board[1][-1] = "G"          # goal tile middle far right

    return ["".join(x) for x in board]


def board_to_map(board):
    return ["".join(x) for x in board]


class RockyRoad(object): 
    """
        RockyRoad involves moving from Start(S) to Goal(G) by avoiding user chosen "bad" terrain, and preferably 
        moving through the "good" terrain.

        The agent can only ever choose to move forward, but it can choose between different modes of execution (more risky or less risky).

        The agent may not always move in the intended direction due to the uneven nature of the terrain. 
        The agent can thus still end up in forbidden terrain. 

        ### Terrain types
        User chooses terrain types. Examples and default: 
        Example terrains:
            * Asphalt ("A") (default)
            * Lawn ("L")
            * Cobbles ("C")
            * Pothole ("H") (default)
        Default terrains:
            * Good: 
                - Asphalt ("A")
            * Bad:
                - Pothole ("H")
        
        The user is free to include more terrain types. 
        Just keep in mind that "G" and "S" are already taken to represent the goal and start cell, respectively. 

        ### Action Space
        The agent takes a 1-element vector for actions.
        The action space is `(dir)(mode)`, where `dir` decides direction to move in and `mode` how risky/safe the action is executed. 
        - RIGHT0
        - RIGHT1
        - RIGHT2
        ...
        - RIGHTM

        ### Observation Space
        The observation is a value representing the agent's current position as
        current_row * num_rows + current_col (where both the row and col start at 0).

        The map always consist of three rows times a user defined set of columns c. 
        The goal position in every map is in position (1, c-1).
        The start position in every map is in position (1, 0).

        ### Rewards
        Rewards may be user defined and included in the environment_info. The default reward schedule is:
        - Reach goal(G): +10

        ### Arguments
        ```
        `length`: int 
        length of road (the number of columns in map)

        `is_uneven`: boolean 
        If True, the agent will move in intended direction with
        a user specified probability, else will move in either perpendicular direction with
        equal probability in both directions.
            For example, if action is right and is_uneven is True, then:
            - P(move right) = 1/2
            - P(move up) = 1/4
            - P(move down) = 1/4

        `bouncing_states`: boolean
        If True, the agent will immediately bounce back from failure states to nominal states. 
        Severity will be added in the environment wrapper.
    """

    def __init__(self, environment_info, bouncing_states=True, use_preset_map=False, is_uneven=True, map=None):
        # BUILD ROCKY ROAD
        self.environment_info = environment_info
        self.allowed_terrains_info = {}
        self.forbidden_terrains_info = {}

        self.unpack_environment_info()
        
        # SET UP STATE SPACE
        length = environment_info["length"]
        map_name = f"3x{length}"
        self.size = length 

        if not map:
            if use_preset_map and map_name in ROAD_MAPS:
                map = ROAD_MAPS[map_name]
            else:
                map = generate_random_road_map(length, self.allowed_terrains_info, self.forbidden_terrains_info)
        else:
            map = map

        self.map = np.asarray(map, dtype="c")
        self.map_size = map_name 

        self.num_rows, self.num_cols = num_rows, num_cols = self.map.shape 
        self.states = [(row, col) for row in range(num_rows) for col in range(num_cols)]
        self.num_states = num_states = num_rows*num_cols
        self.goal_states = [(1, length-1)]
        self.forbidden_states = [state for state in self.states if state[0] == 0 or state[0] == 2]
        self.terminal_states = []
        self.bouncing_states = [state for state in self.states if state[0] != 1] if bouncing_states else []
        self.s0 = (1,0)

        # SET UP ACTION SPACE
        self.num_actions = num_actions = environment_info["num_actions"]
        self.actions = np.arange(self.num_actions)
        self.action_info = {action: {} for action in self.actions}
        self.action_setup()

        # SET UP TRANSITION DYNAMICS AND REWARDS
        self.r_goal = environment_info["goal_reward"]
        self.T = np.zeros((num_states, num_actions, num_states))
        self.R = np.zeros((num_states, num_actions, num_states))
        self.failure_transitions = {state: {} for state in self.states}

        self.build_mdp()

        # SEVERITY INFO (if any)
        if "severity_levels" in environment_info:
            self.severity_levels = environment_info["severity_levels"]
            self.severity_map = {}
            num_sev_lvls = len(self.severity_levels)
            self.T_sev = np.zeros((num_states, num_actions, num_states, num_sev_lvls))
            self.build_severity_maps()
        
        logging.info("Rocky Road environment initialized.")



    def unpack_environment_info(self):
        self.terrain_types = self.environment_info["terrains"]
        for terrain in self.terrain_types:
            if self.environment_info[terrain]["type"] == "forbidden":
                self.forbidden_terrains_info[terrain] = self.environment_info[terrain]["p"]

            elif self.environment_info[terrain]["type"] == "allowed":
                self.allowed_terrains_info[terrain] = self.environment_info[terrain]["p"]

    
    def action_setup(self): 
        """
            safest action is most expensive, riskiest action is cheapest.
            risky decline factor to adjust success rate based on risk level of action. 

            Add ons: 
                * performance decline factors (in case of severities)
                * riskier (cheaper) actions decline faster/at a higher rate
                * factor skewing severity probabilities depending on action
        """

        nom_success_rate = self.environment_info["nom_success_rate"]
        risky_decline_factor = self.environment_info["risky_decline_factor"]
        severity_decline_factor = self.environment_info["severity_decline_factor"]
        skew_factor = self.environment_info["skew_factor"]

        #cost_incr = self.environment_info["action_cost_increment"]

        # order action costs from high to low
        action_costs = sorted(self.environment_info["action_costs"], reverse=True)

        for action in self.actions: 
            cost = action_costs[action]
            success_rate = nom_success_rate*(risky_decline_factor**action)
            performance_decline_factor = severity_decline_factor**(action + 1)
            action_skew_factor = skew_factor**action 

            self.action_info[action] = {"cost": cost, 
                                        "success_rate": success_rate,
                                        "performance_decline_factor": performance_decline_factor, 
                                        "skew_factor": skew_factor, 
                                        "direction": RIGHT
                                        }
            
        self.action_names = {action: f"Right {action}" for action in self.actions}
    


    def build_mdp(self):
        self.build_transition_matrix()
        self.build_reward_matrix()


    def build_transition_matrix(self):
        directions = [RIGHT, UP, DOWN]
        for (sidx, state) in enumerate(self.states):
            if state in self.goal_states:
                self.T[sidx, :, sidx] = 1 

            elif state in self.bouncing_states:
                next_state = self.bounce_state(state)
                next_sidx = self.states.index(next_state)
                self.T[sidx, :, next_sidx] = 1

            else: 
                row, col = state 

                for action in self.actions: 
                    p_success = self.action_info[action]["success_rate"]
                    p_fail = 1 - p_success 
                    failure_transitions = []

                    for direction in directions:
                        p = p_success if direction == RIGHT else p_fail/(len(directions)-1)
                        
                        next_state = self.get_next_state(state, direction)

                        next_state = self.get_next_state(state, direction)
                        next_sidx = self.states.index(next_state)
                        self.T[sidx, action, next_sidx] += p

                        # unsuccessful transition
                        if direction != RIGHT:
                            failure_transitions.append(next_state)
                    
                    self.failure_transitions[state][action] = failure_transitions



    def build_reward_matrix(self):
        for (sidx, state) in enumerate(self.states):
            # no reward in starting from a goal state or bouncing state
            if state not in self.goal_states and state not in self.bouncing_states:
                for action in self.actions: 
                    cost = self.action_info[action]["cost"]
                    reward = -cost 
                    next_state_idxs = np.where(self.T[sidx, action] != 0)[0]
                    for next_state_idx in next_state_idxs:
                        self.R[sidx, action, next_state_idx] += reward 
                        next_state = self.states[next_state_idx]
                        if next_state in self.goal_states:
                            self.R[sidx, action, next_state_idx] += self.r_goal


    def build_severity_maps(self):
        for (sidx, state) in enumerate(self.states):
            terrain = str(bytes(self.map[state]).decode())
            if terrain in self.environment_info and self.environment_info[terrain]["type"] == "forbidden":
                severity_probs = np.array([i for i in self.environment_info[terrain]["nom_sev_probs"]])
                self.severity_map[state] = severity_probs

        for (sidx, state) in enumerate(self.states):
            for action in self.actions: 
                next_sidxs = np.where(self.T[sidx, action] != 0)[0]
                for next_sidx in next_sidxs:
                    next_state = self.states[next_sidx]
                    if next_state in self.severity_map:
                        self.T_sev[sidx, action, next_sidx] = self.severity_map[next_state]

        
                
    def get_next_state(self, state, direction):
        row, col = state 

        if direction == RIGHT:
            col = min(col+1, self.num_cols-1)
        elif direction == UP:
            row = max(row-1, 0)
        elif direction == DOWN:
            row = min(row+1, self.num_rows-1)

        return (row, col)


    def bounce_state(self, state):
        row, col = state 
        return (1, col)
    

    def get_alt_actions(self, action):
        alt_actions = [action, "up", "down"]
        return alt_actions

