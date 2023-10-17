if __name__ == "__main__":
    crossovers = [
        (0.7, 0.8, 0.9, 1.0),
        (0.8, 0.7, 0.9, 1.0),
        (0.9, 0.7, 0.8, 1.0),
        (1.0, 0.7, 0.8, 0.9),
    ]
    repetitions = 10
    partitions = ["batch", "long"]
    print(f"The crossover configuration are {crossovers}")
    for cx1, cx2, cx3, cx4 in crossovers:
        for partition in partitions:
            for rep in range(repetitions):
                with open(
                    f"mea_heuristics_cx1_{cx1}_repetition_{rep}_partition_{partition}.slurm",
                    "w",
                ) as f:
                    f.write(
                        f"""#!/bin/bash
#SBATCH --job-name=mga_{cx1}_{rep}
#SBATCH --time=72:00:00
#SBATCH -N 1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --network=IB
#SBATCH --partition={partition}
#SBATCH --mail-user=amarrerd@ull.edu.es
#SBATCH --mail-type=ALL
        
# Setup the batch environment
source /etc/profile.d/profile.modules.sh

module load gcc/10.2.0
module load openmpi/3.1.4/gcc
module load openssl/1.1.1k/gcc
module load python/3.7.9/gcc
module load bzip2/1.0.8/gcc
module load xz/5.2.5/gcc
module load boost/1.75.0/gcc

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Expected params are <cx1> <cx2> <cx3> <cx4> <fr> <nr> <repetition_idx>

# srun to launch the executable
srun /home/amarrerd/data/dignea/bin/MEAKPExperiment {cx1} {cx2} {cx3} {cx4} 0.85 0.15 {rep}"""
                    )
