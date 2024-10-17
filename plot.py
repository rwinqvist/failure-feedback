import json
import matplotlib.pyplot as plt
import math
import numpy as np

plt.rcParams.update(plt.rcParamsDefault)
plt.rcParams['text.usetex'] = True
plt.rcParams['lines.linewidth'] = 2.0  # Set the desired line width
plt.rcParams['font.size'] = 14  # Set the desired font size


def shaded_plot(lengths, v, num_maps, num_sims, heuristics, path):
    fig1, fig2 = plt.figure(), plt.figure()
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)
    
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas = list(0.1*np.ones(3))
    markers = ['-o', '-s', '-D']
    ms = 8

    for (hix, heuristic) in enumerate(heuristics):
        xs = np.array(lengths)
        ys_sc, ys_fr = [], []
        std_fr, std_sc = [], []

        for length in lengths:
            fn = path + f"ENV{length}_{v}_EXP{length}_{v}_{num_maps}maps_{num_sims}sims.json"
            with open(fn, "r") as json_file: 
                data = json.load(json_file)[heuristic]
                
            map_sc, map_fr = [], []

            for map in range(num_maps):
                rewards = data[f"{map}"]["rewards"]
                step_count = data[f"{map}"]["step_count"]
                failure_count = data[f"{map}"]["failure_count"]

                failure_rate = np.array(failure_count)/np.array(step_count)
                rel_reward_fr = np.array(rewards)/failure_rate
                rel_reward_sc = np.array(rewards)/np.array(step_count)

                map_fr.append(np.mean(rel_reward_fr))
                map_sc.append(np.mean(rel_reward_sc))

            ys_sc.append(np.mean(map_sc))
            ys_fr.append(np.mean(map_fr))

            std_fr.append(np.std(map_fr)) 
            std_sc.append(np.std(map_sc))
        
        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        
        c = default_colors[hix]
        a = alphas[hix]

        label = rf'$\mathrm{{{heuristic}}}$'
        if heuristic == "alg":
            label = r"$\mathrm{FTQ}$"

        marker = markers[hix]
        ax_fr.plot(xs, ys_fr, marker, color=c, label=label, ms=ms)
        ax_fr.fill_between(xs, ys_fr - std_fr, ys_fr + std_fr, color=c, alpha=a)
        ax_sc.plot(xs, ys_sc, marker, color=c, label=label, ms=ms)
        ax_sc.fill_between(xs, ys_sc - std_sc, ys_sc + std_sc, color=c, alpha=a)

    #ax_sc.legend([rf"{heuristic}" for heuristic in heuristics]) 
    #ax_fr.legend([rf"{heuristic}" for heuristic in heuristics]) 
    #ax_fr.legend(heuristics) 
    #plt.yscale('log')
    ax_sc.legend()
    ax_fr.legend()
    ax_sc.set_xlabel(r"$\mathrm{Road\ length,\ } L$")
    ax_sc.set_ylabel(r"$\mathrm{Average\ relative\ reward,\ } \tilde{r}$")
    plt.show(block=True)


def box_plot(lengths, v, num_maps, num_sims, heuristics, path):
    fig1, fig2 = plt.figure(), plt.figure()
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)
    for heuristic in heuristics:
        xs = np.array(lengths)
        ys_sc, ys_fr = [], []
        q1_fr, q3_fr, q1_sc, q3_sc = [], [], [], []


        for length in lengths:
            fn = path + f"ENV{length}_{v}_EXP{length}_{v}_{num_maps}maps_{num_sims}sims.json"
            with open(fn, "r") as json_file: 
                data = json.load(json_file)[heuristic]
                
            map_sc, map_fr = [], []

            for map in range(num_maps):
                rewards = data[f"{map}"]["rewards"]
                step_count = data[f"{map}"]["step_count"]
                failure_count = data[f"{map}"]["failure_count"]

                failure_rate = np.array(failure_count)/np.array(step_count)
                rel_reward_fr = np.array(rewards)/failure_rate
                rel_reward_sc = np.array(rewards)/np.array(step_count)

                map_fr.append(np.mean(rel_reward_fr))
                map_sc.append(np.mean(rel_reward_sc))

            ys_sc.append(np.mean(map_sc))
            ys_fr.append(np.mean(map_fr))

            q1_fr.append(np.percentile(map_fr, 25)) 
            q3_fr.append(np.percentile(map_fr, 75)) 
            q1_sc.append(np.percentile(map_sc, 25)) 
            q3_sc.append(np.percentile(map_sc, 75)) 

        
        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        q1_fr, q3_fr, q1_sc, q3_sc = np.array(q1_fr), np.array(q3_fr), np.array(q1_sc), np.array(q3_sc)
        ax_fr.errorbar(xs, ys_fr, yerr=[ys_fr - q1_fr, q3_fr - ys_fr], capsize=10, elinewidth=2)
        ax_sc.errorbar(xs, ys_sc, yerr=[ys_sc - q1_sc, q3_sc - ys_sc], capsize=10, elinewidth=2)

    ax_sc.legend([rf"{heuristic}" for heuristic in heuristics]) 
    ax_fr.legend([rf"{heuristic}" for heuristic in heuristics]) 
    #ax_fr.legend(heuristics) 
    #plt.yscale('log')
    plt.show(block=False)



def mc_mean_plot(lengths, v, num_maps, num_sims, heuristics, path): 
    fig1, fig2 = plt.figure(), plt.figure()
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)
    for heuristic in heuristics:
        xs = np.array(lengths)
        ys_sc, ys_fr = [], []

        for length in lengths:
            fn = path + f"ENV{length}_{v}_EXP{length}_{v}_{num_maps}maps_{num_sims}sims.json"
            with open(fn, "r") as json_file: 
                data = json.load(json_file)[heuristic]
                
            map_sc, map_fr = [], []

            for map in range(num_maps):
                rewards = data[f"{map}"]["rewards"]
                step_count = data[f"{map}"]["step_count"]
                failure_count = data[f"{map}"]["failure_count"]

                failure_rate = np.array(failure_count)/np.array(step_count)
                rel_reward_fr = np.array(rewards)/failure_rate
                rel_reward_sc = np.array(rewards)/np.array(step_count)

                map_fr.append(np.mean(rel_reward_fr))
                map_sc.append(np.mean(rel_reward_sc))

            ys_sc.append(np.mean(map_sc))
            ys_fr.append(np.mean(map_fr))

        ax_sc.plot(xs, ys_sc, "-o", label=f"{heuristic}")
        ax_fr.plot(xs, ys_fr, "-o", label=f"{heuristic}")

    ax_sc.legend() 
    ax_fr.legend() 
    plt.show(block=False)


def qcost_plot(path, length, v, qcosts, num_maps, num_sims, heuristics=["alg", "always", "never"]): 
    fig1, fig2 = plt.figure(), plt.figure()
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas = list(0.1*np.ones(3))
    markers = ['-o', '-s', '-D']
    ms = 8

    for (hix, heuristic) in enumerate(heuristics):
        xs = np.array(qcosts)
        ys_sc, ys_fr = [], []
        std_fr, std_sc = [], []

        for qcost in qcosts: 
            fn = path + f"ENV{length}_{v}_EXP{length}_{v}_{num_maps}maps_{num_sims}sims_qcost_{qcost}.json"
            with open(fn, "r") as json_file: 
                data = json.load(json_file)[heuristic]

            map_sc, map_fr = [], []

            for map in range(num_maps):
                rewards = data[f"{map}"]["rewards"]
                step_count = data[f"{map}"]["step_count"]
                failure_count = data[f"{map}"]["failure_count"]

                failure_rate = np.array(failure_count)/np.array(step_count)
                rel_reward_fr = np.array(rewards)/failure_rate
                rel_reward_sc = np.array(rewards)/np.array(step_count)

                map_fr.append(np.mean(rel_reward_fr))
                map_sc.append(np.mean(rel_reward_sc))

            ys_sc.append(np.mean(map_sc))
            ys_fr.append(np.mean(map_fr))

            std_fr.append(np.std(map_fr)) 
            std_sc.append(np.std(map_sc))
        
        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        
        c = default_colors[hix]
        a = alphas[hix]

        label = rf'$\mathrm{{{heuristic}}}$'
        if heuristic == "alg":
            label = r"$\mathrm{FTQ}$"

        marker = markers[hix]
        ax_fr.plot(xs, ys_fr, marker, color=c, label=label, ms=ms)
        ax_fr.fill_between(xs, ys_fr - std_fr, ys_fr + std_fr, color=c, alpha=a)
        ax_sc.plot(xs, ys_sc, marker, color=c, label=label, ms=ms)
        ax_sc.fill_between(xs, ys_sc - std_sc, ys_sc + std_sc, color=c, alpha=a)

    ax_sc.legend()
    ax_fr.legend()
    ax_sc.set_xlabel(r"$\mathrm{Query\ cost,\ } q_c$")
    ax_sc.set_ylabel(r"$\mathrm{Average\ relative\ reward,\ } \tilde{r}$")
    plt.show(block=True)



def failcount_vs_stepcount(path, lengths, v, num_maps, num_sims, heuristics = ["alg", "always", "never"]):
    fig1, fig2 = plt.figure(), plt.figure()
    ax_sc, ax_fr = fig1.add_subplot(111), fig2.add_subplot(111)
    
    default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    alphas = list(0.1*np.ones(3))
    markers = ['-o', '-s', '-D']
    ms = 8

    for (hix, heuristic) in enumerate(heuristics):
        xs = np.array(lengths)
        ys_sc, ys_fr = [], []
        std_fr, std_sc = [], []

        for length in lengths:
            fn = path + f"ENV{length}_{v}_EXP{length}_{v}_{num_maps}maps_{num_sims}sims.json"
            with open(fn, "r") as json_file: 
                data = json.load(json_file)[heuristic]
                
            map_sc, map_fr = [], []

            for map in range(num_maps):
                rewards = data[f"{map}"]["rewards"]
                step_count = data[f"{map}"]["step_count"]
                failure_count = data[f"{map}"]["failure_count"]

                failure_rate = np.array(failure_count)/np.array(step_count)

                map_fr.append(np.mean(failure_rate))
                map_sc.append(np.mean(failure_rate))

            ys_sc.append(np.mean(map_sc))
            ys_fr.append(np.mean(map_fr))

            std_fr.append(np.std(map_fr)) 
            std_sc.append(np.std(map_sc))
        
        ys_fr, ys_sc = np.array(ys_fr), np.array(ys_sc)
        
        c = default_colors[hix]
        a = alphas[hix]

        label = rf'$\mathrm{{{heuristic}}}$'
        if heuristic == "alg":
            label = r"$\mathrm{FTQ}$"

        marker = markers[hix]
        ax_fr.plot(xs, ys_fr, marker, color=c, label=label, ms=ms)
        ax_fr.fill_between(xs, ys_fr - std_fr, ys_fr + std_fr, color=c, alpha=a)
        ax_sc.plot(xs, ys_sc, marker, color=c, label=label, ms=ms)
        ax_sc.fill_between(xs, ys_sc - std_sc, ys_sc + std_sc, color=c, alpha=a)

    #ax_sc.legend([rf"{heuristic}" for heuristic in heuristics]) 
    #ax_fr.legend([rf"{heuristic}" for heuristic in heuristics]) 
    #ax_fr.legend(heuristics) 
    #plt.yscale('log')
    ax_sc.legend()
    ax_fr.legend()
    ax_sc.set_xlabel(r"$\mathrm{Road\ length,\ } L$")
    ax_sc.set_ylabel(r"$\mathrm{Failure\ rate,\ } F_r$")
    plt.show(block=True)




def main(): 
    env = "rocky_road"
    path = f"exp_data_2/{env}/"

    lengths = [15, 20, 25, 30, 35, 40]
    v = 1
    num_maps = 10 
    num_sims = 100

    heuristics = ["alg", "always", "never"]
 
    #mc_mean_plot(lengths, v, num_maps, num_sims, heuristics, path)
    #box_plot(lengths, v, num_maps, num_sims, heuristics, path)
    #shaded_plot(lengths, v, num_maps, num_sims, heuristics, path)
    #failcount_vs_stepcount(path, lengths, v, num_maps, num_sims)

    length = 40
    v = 4
    num_maps = 10 
    num_sims = 100
    qcosts = [0, 5, 10, 20, 30, 40]
    qcost_plot(path, length, v, qcosts, num_maps, num_sims)


if __name__ == "__main__":
    main()