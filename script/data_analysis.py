#!/usr/bin/python3

from os import listdir
import numpy as np
import argparse
import re
import json
import pandas as pd


def parse_files(path, inst_regex, verbose=False):
    """
    Parses a JSON file from a MEA experiment to generate two dataset with the following data
    1. A difference dataset comparing the target-Ox configuration difference in performance to some generated instances
    2. A dataset with all the results for each repetition over every single instance generated

    It also generates the .allHV files used in METCO to statistical analysis
    """

    dfs_diffs = []
    dfs_raws = []
    n_instances = 0  # This is the index in the results files and dfs
    for file in listdir(path):
        # Buscamos todos los ficheros de resultados para la instancia concreta
        if re.match(inst_regex, file):
            with open(f"{path}/{file}") as f:
                j_file = json.load(f)
            print(f"Opening filename: {file}")
            # Getting the algorithm's names for the columns
            algs_names = [
                f'GA_{round(target["crossover_rate"], 3)}'
                for target in j_file["algorithm"]["portfolio"]
            ]
            # algs_names = list(
            #    map(
            #        lambda alg: alg["name"].replace(" KP", ""),
            #        j_file["algorithm"]["configurations"],
            #    )
            # )
            # Just interested in the solutions
            front = j_file["front"]
            differences = {}
            raw_results = {}
            indexes = []
            for i in front:
                if i != "n_solutions" and front[i]["biasedFitness"] > 0:
                    avgs = [np.mean(l) for l in front[i]["conf_fitness"]]
                    print(avgs)
                    if all(x > 0 for x in avgs):
                        differences[n_instances] = [avgs[0] - x for x in avgs][1:]
                        if verbose:
                            print(
                                f"Solution {i} Average fitness:\n\t- {avgs}\nAverage differences:\n\t- {differences[i]}\n"
                            )

                        raw_results[n_instances] = front[i]["conf_fitness"]
                        indexes.append(n_instances)
                        # Creates allHVs
                        for j, l in zip(range(4), algs_names):
                            with open(
                                f"instance_{n_instances}_target_{algs_names[0]}_solved_by_{l}.allHV",
                                "w",
                            ) as f:
                                f.write(
                                    "\n".join(map(str, front[i]["conf_fitness"][j]))
                                )
                        n_instances += 1  # New instance parsed

            if len(differences) != 0:
                # Creates a df for the differences between target and others
                df = pd.DataFrame.from_dict(differences).T
                t_Ox_cols = list(
                    map(lambda alg: f"{algs_names[0]}-{alg}", algs_names[1:])
                )
                df.columns = t_Ox_cols
                df.index = indexes
                # Creates a df with all the values RAW
                df_raw = pd.DataFrame.from_dict(raw_results).T
                df_raw.columns = algs_names
                df_raw.index = indexes

                dfs_diffs.append(df)
                dfs_raws.append(df_raw)
    print(dfs_diffs)
    if len(dfs_diffs) != 0:
        return dfs_diffs, dfs_raws, algs_names[0]
    else:
        return None, None, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Data analysis")
    parser.add_argument("path", type=str, help="Path to find the .json result files")

    args = parser.parse_args()
    path = args.path

    inst_regex = rf".*\.json"
    dfs_diffs, dfs_raw, target_alg = parse_files(path, inst_regex)
    if dfs_diffs is not None:
        df_diff = pd.concat(dfs_diffs)
        df_raw = pd.concat(dfs_raw)
        df_diff = df_diff.sort_index()
        df_raw = df_raw.sort_index()
        df_diff.to_csv(f"differences_mea_kp_verification_{target_alg}.csv")
        df_raw.to_csv(f"mea_kp_ns_verification_target_{target_alg}.csv")
