import json
import matplotlib.pyplot as plt
import math
import numpy as np

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True

env = "rocky_road"
type = "length"
path = f"mc_data/{env}/{type}/"

date = "2024-08-09"
filenum = 3
filename = f"{date}_{filenum}.json"

with open(path+filename, "r") as data_file:
    data = json.load(data_file)

lengths = data["lengths"]
num_maps = data["num_maps"]
num_episodes = data["num_episodes"]
env_info = data["env_info"]
exp_info = data["exp_info"]

map_num = 1
ys = []

xs, ys = [], []

for length in lengths: 
    xs.append(length)
    results = data[f"length_{length}"][f"map_{map_num}"]["results"]
    query_rates = np.array(results["query_rates"])
    query_rates = query_rates[~np.isnan(query_rates)]
    avg_query_rate = np.sum(query_rates)/len(query_rates)
    ys.append(avg_query_rate)

plt.plot(xs, ys)
plt.show()
