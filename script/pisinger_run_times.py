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
import shutil
from collections import defaultdict


def get_selected_instances(path):
    from_path = (
        "/home/amarrero/ns_kp_journal/jsons/revision_1/threshold_evaluation/Random/"
    )
    destination_path = (
        "/home/amarrero/ns_kp_journal/jsons/revision_1/threshold_evaluation/selected/"
    )
    for file in listdir(path):
        instance_file = file.split("_results")[0]
        instance_file = instance_file.split("Instance_")[1]
        full_file_path = from_path + instance_file
        destination_full = destination_path + instance_file
        print(f"From: {full_file_path}")
        shutil.copy(full_file_path, destination_full)
        print(instance_file)


def get_average_runtimes(path):
    run_times = []
    for file in listdir(path):
        instance_file = file.split("_results")[0]
        instance_file = instance_file.split("Instance_")[1]
        print(f"File: {file}")
        with open(join(path, file), "r") as file_handler:
            data = json.load(file_handler)
            # average_expKnap = np.mean(np.array(data["expTimes"]))
            # average_minKnap = np.mean(np.array(data["minKnap"]))
            # run_times.append([average_expKnap, average_minKnap])
            best_fit = data["BestFit"]
            first_fit = data["FirstFit"]
            next_fit = data["NextFit"]
            worst_fit = data["WorstFit"]

            run_times.append([best_fit, first_fit, next_fit, worst_fit])

    run_times = np.asarray(run_times)
    print(run_times)
    # np.savetxt("runtimes_expknap_minknap.txt", run_times)
    np.savetxt("fitness_best_first_next_worst.txt", run_times)
    return run_times


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dataset generator")
    parser.add_argument("path", type=str, help="Path to find the .json result files")

    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()
    path = args.path
    # get_selected_instances(path)
    get_average_runtimes(path)
