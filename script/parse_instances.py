import pandas as pd
from os import walk
from os.path import join
import argparse
import re
import numpy as np

KP_EXT = ".kp"
COLS = [
    "N",
    "Q",
    "class",
    "R",
    "avg_eff",
    "max_p",
    "max_w",
    "mean_weight_norm",
    "median_weight_norm",
    "std_weight_norm",
    "mean_profit_norm",
    "median_profit_norm",
    "std_profit_norm",
    "corr_p_w",
]
"""
    Caracteristicas Empleadas por C.Coello
    - Mean weight value / maximum weight
    - Median weight value / maximum weight
    - Standard deviation of weights / maximum weight
    - Mean profit value / maximum profit
    - Median profit value / maximum profit
    - Standard deviation of profits / maximum profit
    - Correlation weight-profit / 2 and shifted 0.5.
"""


def get_list_of_files(path=None):
    """
    Buscamos en los directorios dentro de path para encontrar todas
    las instancias del problema de la mochila
    :param path:
    :return:
    """
    instances = []
    for root, dirs, files in walk(path):
        for file in files:
            # if file.endswith(KP_EXT):
            instances.append(join(root, file))
    return instances


def parse_instance(file=None):
    """
    Parseamos el contenido de una instancia para obtener sus caracteristicas
    :param file:
    :return:
    """
    print(f"File is: {file}")
    instance = []
    instance_data = []
    # Obtenemos los parametros de la instancia a partir de su nombre
    params = re.split("/", file)[-1].split("_")
    with open(file) as f:
        instance_data = f.readlines()

    weights = []
    profits = []
    chromosome = []
    for line in instance_data[2:]:
        weight, profit = line.split()
        w = int(weight)
        p = int(profit)
        weights.append(w)
        profits.append(p)
        chromosome.append(p)
        chromosome.append(w)

    print(f"Len(w): {len(weights)} and Len(p): {len(profits)}")
    capacity = int(instance_data[0].split()[1])  # 1 for common 2 for Smith Miles
    max_p = np.max(profits)
    max_w = np.max(weights)
    min_p = np.min(profits)
    min_w = np.min(weights)
    mean = np.mean(chromosome)
    std = np.std(chromosome)
    avg_eff = 0.0
    for profit, weight in zip(profits, weights):
        if weight == 0:
            continue
        avg_eff += profit / weight

    instance = {
        "target": "Random",  # instance_data[1].split()[0],  # params[0],
        "capacity": capacity,
        "avg_eff": avg_eff,
        "max_p": max_p,
        "max_w": max_w,
        "mean": mean,
        "min_p": min_p,
        "min_w": min_w,
        "std": std,
    }

    for i, profit in zip(range(len(profits)), profits):
        instance[f"p_{i}"] = profit

    for i, weight in zip(range(len(profits)), weights):
        instance[f"w_{i}"] = weight

    return instance


def generate_dataset(path, filename="knapsack_dataset.csv"):
    files = get_list_of_files(path)
    if len(files) == 0:
        print(f"No files found in {path}")
    else:
        print(f"Found {len(files)} instances")
        instances = []
        for file in files:
            instances.append(parse_instance(file))

        dataset = pd.DataFrame(instances)
        print(f"Dataset generated.")
        print("=" * 80)
        print(dataset.head())

        dataset.to_csv(filename, index=False)
        return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Knapsack DataFrame Generator")
    parser.add_argument("path", help="Root dir of the instances")
    parser.add_argument("-f", "--file", help="Output file")
    args = parser.parse_args()
    filename = "knapsack_dataset.csv" if args.file is None else args.file
    dataset = generate_dataset(args.path, filename)
