#!/bin/python3
"""
    Updated version of the generate df script.
    v1.5.0
"""
from typing import Callable
import pandas as pd
from os import listdir
from os.path import join
import argparse
import json
import numpy as np


def open_file_and_get_front(filename: str, verbose=True) -> pd.DataFrame:
    """
    Opens the JSON file from MEA and returns a pd.DataFrame
    with the necessary front information

    The target_name must be updated to reflect the algorithms used in the experimentation.

    """
    if verbose:
        print(f"Opening file: {filename}")

    with open(filename, "r") as file:
        data = json.load(file)
        front = data["front"]
        target = data["algorithm"]["portfolio"][0]
        # target_name = filename.split("_")[2]
        # TODO: Update if necessary
        # target_name =  f'GA_{round(target["crossover_rate"], 3)}'
        target_name = target["name"].replace(" TSP", "")

    # Temporarly including performance data
    names = [
        alg["name"].replace(" TSP", "")
        for alg in data["algorithm"]["portfolio"]
        # f'GA_{round(alg["crossover_rate"], 3)}'
        # for alg in data["algorithm"]["configurations"]
    ]
    for i in front:
        if i != "n_solutions":
            if front[i]["biasedFitness"] < 0.0:
                continue
            # avgs = np.mean(front[i]["conf_fitness"])
            avgs = [np.mean(l) for l in front[i]["conf_fitness"]]
            for alg, value in zip(names, avgs):
                # print(f"Algorithm: {alg} with value: {value}")
                front[i][alg] = value
            front[i]["target_performance"] = avgs[0]
            # Only for MOMEA
            # front[i]["performance_score"] = front[i]["objs"][0]
            # front[i]["novelty_score"] = front[i]["objs"][1]

    if front["n_solutions"] != 0:
        df = pd.DataFrame.from_dict(front).T
        df.drop(["n_solutions"], inplace=True)
        # df["ns_threshold"] = data["algorithm"]["novelty_search"]["threshold"]
        df = pd.concat([df, df["features"].apply(pd.Series)], axis=1)
        df.insert(0, "target", target_name)

        return df
    else:

        return None


def generate_dataset(
    path: str, c_features: Callable = None, verbose: bool = True
) -> pd.DataFrame:
    """
    Generates a dataset by parsing the JSON files from the MEA executions
    Goes through each JSON file in the directory and gets the useful information

    - c_features is a function with receives a pd.DataFrame as argument and returns
        another pd.DataFrame with custom features which may be problem dependent. If
        it is not ncessary, just set to None
    """
    dfs = []
    stats = []  # Number of instances generated for repetition
    for file in listdir(path):
        if not file.endswith(".json"):
            continue
        fname = join(path, file)
        front = open_file_and_get_front(fname)
        if verbose:
            print(f"File: {file}")
        if front is not None:
            if c_features is not None:
                front = c_features(front)

            #         # Temporarly calculated instances per run

            #         stats.append(len(front.index))

            #         if verbose:
            #             print(front.head())
            dfs.append(front)

    temp = pd.concat(dfs, ignore_index=True)
    temp = temp.dropna()
    # print(stats)
    # s = pd.Series(stats)
    # print(s.describe())

    return temp


def c_features_tsp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Includes custom features for each instance in the df
    This function is now particularly useful for the TSP
    For other problems must be omitted
    """
    coords_grouped = []
    for a in df.coords.to_list():
        coords_grouped.append(list(zip(*[iter(a)] * 2)))

    coords_df = pd.DataFrame(df.coords.tolist(), df.index).add_prefix("c_")

    df = df.join([coords_df])
    df.drop(
        [
            "n_vars",
            "features",
            "fitness",
            "biasedFitness",
            "conf_fitness",
            "diversity",
            "coords",
        ],
        axis=1,
        inplace=True,
        errors="ignore",
    )
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset generator")
    parser.add_argument("path", type=str, help="Path to find the .json result files")
    parser.add_argument(
        "output_filename", type=str, help="Filename of the resulting CSV file"
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    path = args.path

    filename = args.output_filename
    df = generate_dataset(path, c_features_tsp, verbose=args.verbose)
    df.to_csv(filename, index=False)

    if args.verbose:
        print(df.head())
