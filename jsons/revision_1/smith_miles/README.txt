The Original_Instances folder contains instances based on instance classes which were used to generate an initial instance space. The PostGA_Instances folder contains the instances produced by a genetic algorithm to fill holes in the earlier space. Both sets of instances combined are used to produce the final version of the instance space.

File format is as follows...
Line 1: Instance name
Line 2: Instance class (or placeholder for some GA instances)
Line 3: Knapsack Capacity:
Later lines: Knapsack item weight then value, one item on each line

The algorithm code attached is a slightly modified version of the C code written by Pisinger et al. for these algorithms, intended to facilitate reliable measurement of runtime and graceful termination of EXPKNAP when it runs for a long time. See the individual source code files for more details. You'll probably need to do some tweaking to get this to work for you.

The *output.txt files in this directory contain observed runtime data for each algorithm and instance. These are used in addition to the instance files themselves to produce a table of metadata containing both feature and performance data to be used by MATILDA.

metadata_allfeatures.csv is a copy of the metadata file produced by the feature extraction code which includes all features (from which MATILDA can select a good subset based on its parameters).