# %%
from collections import defaultdict
import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %%
if __name__ == "__main__":
    path = "../jsons/revision_1/parameter_tuning_eas/evolution/"
    groups = defaultdict(list)
    for filename in os.listdir(path):
        basename, extension = os.path.splitext(filename)
        instance = (basename.split(".")[-2]).split("_")
        instance = "_".join(instance[-5:])
        if extension == ".DP":
            algorithm = "DP"
            with open(os.path.join(path, filename)) as f:
                evolution = float(f.readline())
        else:
            tokens = basename.split("_")
            algorithm = tokens[0] + "_" + tokens[1]
            with open(os.path.join(path, filename)) as f:
                data = json.load(f)
                evolution = list(data["evolution"])

        tag = f"{instance}-N-{1000}"
        groups[tag].append((algorithm, evolution))

    x_ticks = np.arange(0, 5e4, step=128)

    # %%
    plt.figure(figsize=(12, 8))

    for instance in groups:
        for alg, evolution in groups[instance]:
            x_axis = np.arange(0, len(evolution))
            plt.plot(x_ticks[:-1], evolution, label=alg)

        plt.title(f"Evolution of GAs for {instance}")
        plt.legend()
        plt.show()

# %%
