import pandas as pd
from os import walk
from os.path import join
import argparse
import re
import numpy as np
from sklearn.preprocessing import StandardScaler

BPP_EXT = ".bpp"

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

    weights = [int(line) for line in instance_data[2:]]

    print(f"Len(w): {len(weights)}")
    capacity = int(instance_data[0].split()[1])  # 1 for common 2 for Smith Miles

    normalised_weights = StandardScaler().fit_transform(
        np.array(weights).reshape(-1, 1)
    )
    proportions = dict(huge=0, medium=0, large=0, small=0, tiny=0)
    for w in normalised_weights:
        if w > 0.5:
            proportions["huge"] += 1
        elif w > 0.333 and w <= 0.5:
            proportions["large"] += 1
        elif w > 0.25 and w <= 0.333:
            proportions["medium"] += 1
        elif w > 0.1 and w <= 0.25:
            proportions["small"] += 1
        elif w <= 0.1:
            proportions["tiny"] += 1

    instance = {
        "target": "Random",  # instance_data[1].split()[0],  # params[0],
        "N": len(weights),
        "capacity": capacity,
        "meanW": np.mean(weights),
        "medianW": np.median(weights),
        "varianceW": np.var(weights),
        "maxW": np.max(weights),
        "minW": np.min(weights),
        "huge": proportions["huge"],
        "medium": proportions["medium"],
        "small": proportions["small"],
        "tiny": proportions["tiny"],
    }

    for i, weight in enumerate(weights):
        instance[f"w_{i}"] = weight

    return instance


def generate_dataset(path, filename="bpp_dataset.csv"):
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
    parser = argparse.ArgumentParser(prog="BPP DataFrame Generator")
    parser.add_argument("path", help="Root dir of the instances")
    parser.add_argument("-f", "--file", help="Output file")
    args = parser.parse_args()
    filename = "bpp_dataset.csv" if args.file is None else args.file
    dataset = generate_dataset(args.path, filename)
