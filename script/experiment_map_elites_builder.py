if __name__ == "__main__":
    crossovers = [
        (0.7, 0.8, 0.9, 1.0),
        (0.8, 0.7, 0.9, 1.0),
        (0.9, 0.7, 0.8, 1.0),
        (1.0, 0.7, 0.8, 0.9),
    ]
    repetitions = 10
    bins = [3, 5, 10, 15, 20, 25, 50]
    print(f"The crossover configuration are {crossovers}")
    for cx1, cx2, cx3, cx4 in crossovers:
        for rep in range(repetitions):
            for b in bins:
                with open(
                    f"map_elites_genetics_cx_{cx1}_bins_{b}_repetition_{rep}.slurm", "w"
                ) as f:
                    f.write(
                        f"""#!/bin/bash
#SBATCH --job-name=map_{cx1}_{b}_{rep}
#SBATCH --time=72:00:00
#SBATCH -N 1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --network=IB
#SBATCH --partition=long
#SBATCH --mail-user=amarrerd@ull.edu.es
#SBATCH --mail-type=ALL
        
# Setup the batch environme
source /etc/profile.d/profile.modules.sh

module load gcc/10.2.0
module load openmpi/3.1.4/gcc
module load openssl/1.1.1k/gcc
module load python/3.7.9/gcc
module load bzip2/1.0.8/gcc
module load xz/5.2.5/gcc
module load boost/1.75.0/gcc

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Expected params are <cx1> <cx2> <cx3> <cx4> <fr> <bins> <repetition_idx>

# srun to launch the executable
srun /home/amarrerd/data/dignea/bin/MapElitesKP {cx1} {cx2} {cx3} {cx4} {b} {rep}"""
                    )
