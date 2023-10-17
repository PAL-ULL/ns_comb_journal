import pandas as pd
import numpy as np
import itertools as it


def per_instance(it, is_delimiter=lambda x: x == "-----\n"):
    ret = []
    for line in it:
        if is_delimiter(line):
            if ret:
                yield ret  # OR  ''.join(ret)
                ret = []
        else:
            ret.append(line.rstrip())  # OR  ret.append(line)
    if ret:
        yield ret


def process_instance(instance: list, id: int = 0):
    n = 1000
    with open(f"pisinger_hard_instance_N_{n}_{id}.kp", "w") as f:
        capacity = int(instance[3].split(" ")[-1])
        f.write(f"{n} {capacity}\n\n")
        print(f"Capacity: {capacity}")
        for line in instance[6:]:
            print(line)
            item, profit, weight, _ = line.split(",")
            print(f"Processing item {item} with profit {profit} and weight {weight}")
            f.write(f"{weight} {profit}\n")

        print("Done")


if __name__ == "__main__":
    with open("knapPI_11_1000_1000.csv", "r") as f:
        instances = list(per_instance(f))

        for i in range(len(instances) - 1):
            print(instances[i])
            input()
            process_instance(instances[i], i)
