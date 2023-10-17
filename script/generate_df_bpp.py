#!/bin/python3
"""
    Updated version of the generate df script.
    v1.5.0
"""
from typing import Callable
import pandas as pd
from os import listdir
from os.path import join, isfile
import argparse
import json
import numpy as np


def open_file_and_get_front(
    filename: str, moeig: bool = False, map_elites: bool = False, verbose=True
) -> pd.DataFrame:
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
        target_name = target["name"]

    # Includes performance data
    names = [alg["name"] for alg in data["algorithm"]["portfolio"]]

    for i in front:
        if i != "n_solutions":
            if front[i]["biasedFitness"] < 0.0:  # Also valid for MOEIG
                continue
            avgs = [np.mean(l) for l in front[i]["conf_fitness"]]
            for alg, value in zip(names, avgs):
                # print(f"Algorithm: {alg} with value: {value}")
                front[i][alg] = value
            front[i]["target_performance"] = avgs[0]

            if moeig:
                # Only for MOMEA collect the objectives
                front[i]["performance_score"] = front[i]["objs"][0]
                front[i]["novelty_score"] = front[i]["objs"][1]

    if front["n_solutions"] != 0:
        df = pd.DataFrame.from_dict(front).T
        df.drop(["n_solutions"], inplace=True)
        df = pd.concat([df, df["features"].apply(pd.Series)], axis=1)

        tmp_items = pd.DataFrame(df["items"].values.tolist(), df.index).add_prefix("i_")
        df = df.join([tmp_items])

        df.insert(0, "target", target_name)

        if map_elites:
            bin_resolution = data["algorithm"]["features_info"][0][1][-1]
            df["bin_resolution"] = bin_resolution
        else:
            df["ns_threshold"] = data["algorithm"]["novelty_search"]["threshold"]

        return df
    else:
        return None


def generate_dataset(
    path: str,
    moeig: bool = False,
    map_elites: bool = False,
    c_features: Callable = None,
    include_stats: bool = False,
    verbose: bool = True,
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
        front = open_file_and_get_front(fname, moeig, map_elites)
        if verbose:
            print(f"File: {file}")

        if front is not None:
            if c_features is not None:
                front = c_features(front)

            if include_stats:
                # Includes the number of instances per file (run)
                stats.append(len(front.index))

            dfs.append(front)

    temp_df = pd.concat(dfs, ignore_index=True)
    temp_df = temp_df.dropna()

    s = None
    if include_stats:
        s = pd.Series(stats)
        if verbose:
            print(s.describe())
    return temp_df, s


def c_features_bpp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Includes custom features for each instance in the df
    This function is now particularly useful for the KP
    For other problems must be omitted
    """

    df.drop(
        [
            "n_vars",
            "items",
            "features",
            "Q",
            "fitness",
            "biasedFitness",
            "conf_fitness",
            "diversity",
            "isReducedSpace",
            "cons",
            "const_coeff",
            "crow_distance",
            "num_cons",
            "num_objs",
            "num_vars",
            "objs",
            "rank",
            "vars",
        ],
        axis=1,
        inplace=True,
        errors="ignore",
    )
    return df


def generate_instances(path, verbose=False):
    """
    Function to generate BPP solvable instances
    from the results in the JSON files generated
    after running the MEA
    """
    pass
    # for file in listdir(path):
    #     if not file.endswith(".json"):
    #         continue
    #     fname = join(path, file)
    #     if verbose:
    #         print(f"Openning file: {fname}")
    #     with open(fname, "r") as f:
    #         data = json.load(f)["front"]
    #         n_instances = 0
    #         for inst_ix in data:
    #             if inst_ix != "n_solutions" and float(data[inst_ix]["fitness"]) >= 0.0:
    # n_items = data[inst_ix]["n_vars"] // 2
    # capacity = data[inst_ix]["capacity"]
    # profits = data[inst_ix]["profits"]
    # weights = data[inst_ix]["weights"]
    # w_and_p_str = ""
    # for w, p in zip(weights, profits):
    #     w_and_p_str += f"{w} {p}\n"

    # instance_name = (
    #     file[: file.rfind(".json")] + "_" + str(n_instances) + ".kp"
    # )
    # if verbose:
    #     print(f"Writing to file: {instance_name}")
    # with open(instance_name, "w") as instance_file:
    #     instance_file.write(
    #         f"{n_items} {capacity}\n\n{w_and_p_str[:-1]}"
    #     )
    #     n_instances += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset generator")
    parser.add_argument("path", type=str, help="Path to find the .json result files")
    parser.add_argument(
        "output_filename", type=str, help="Filename of the resulting CSV file"
    )
    parser.add_argument(
        "-m",
        "--multiobjective",
        action="store_true",
        help="Multi-objective flag to parse MOEIG result files",
    )
    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Stats flag to calculate the number of instances per run",
    )

    parser.add_argument(
        "--map_elites",
        action="store_true",
        help="Map-Elites flag to parse MapElites results from DIGNEA",
    )
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    path = args.path

    filename = args.output_filename
    df, stats = generate_dataset(
        path,
        args.multiobjective,
        args.map_elites,
        c_features_bpp,
        include_stats=args.stats,
        verbose=args.verbose,
    )
    df.to_csv(filename, index=False)
    if stats is not None:
        stats_filename = filename.replace(".csv", "_stats.csv")
        stats.describe().to_csv(stats_filename)

    if args.verbose:
        print(df.head())
