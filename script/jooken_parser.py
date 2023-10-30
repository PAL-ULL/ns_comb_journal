from os import path, listdir, walk
import collections

instance_path = "../tmp/problemInstances"
directories = list(
    path.join(instance_path, d) for d in listdir(instance_path) if d.startswith("n_")
)


n_counter = collections.defaultdict(int)
for dir in directories:
    n = dir.split("_")[3]
    idx = n_counter[n]
    pattern = f"Jooken_kp_instance_N_{n}_{idx}.kp"
    print(f"Parsing directory {dir}")
    instance, _, _ = listdir(dir)
    with open(path.join(dir, instance), "r") as file:
        data = file.readlines()
        data = [d.strip() for d in data]
    with open(path.join(path.curdir, pattern), "w") as output:
        output.write(f"{data[0]}\t{data[-1]}\n\n")
        for _, p, w in map(str.split, data[1:-1]):
            output.write(f"{w}\t{p}\n")

    n_counter[n] += 1
