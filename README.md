# A novelty-search approach to filling an instance-space with diverse and discriminatory instances for the knapsack problem

## Authors:

- Alejandro Marrero - amarrerd@ull.edu.es
- Eduardo Segredo - esegredo@ull.edu.es
- Coromoto León - cleon@ull.edu.es
- Emma Hart - e.hart@napier.ac.uk

## Abstract:
In order to gain insight into the relative strengths and weaknesses of a set of algorithms with respect to solving instances from a problem domain, it is necessary to establish a large set of instances that provides good coverage of the potential instance-space.
Gathering sufficient data can be challenging, particularly with respect to finding instances that highlight where some algorithms work well or poorly.
In this paper we propose an approach to generating synthetic instances that are tailored to perform well with respect to a target algorithm belonging to a predefined portfolio. Our approach uses a novelty-search algorithm with a linearly weighted fitness function that balances novelty and performance, to generate a large set of diverse and discriminatory instances in a single run of the algorithm. We consider two definitions of novelty: (1) with respect to discriminatory performance within a portfolio of solvers; (2) with respect to the features of the evolved instances.
We evaluate the proposed method in the Knapsack Problem domain. The said method delivers a set of instances where a particular target algorithm performs better than the remaining solvers in the portfolio. 
In addition, instances are diverse in terms of the relative size of the `performance gap' between the target solver and the remaining ones.
Results show that both novelty-search approaches succeed not only in providing considerably better coverage of the performance and feature spaces, but also obtaining large sets of diverse instances in comparison to an evolutionary method that does not consider novelty.
Moreover, statistical analysis demonstrates that significant differences exist amongst the performance of the target algorithm and the remaining solvers in the portfolio when solving the instances generated for the target approach.
Finally, we show that the method is generalisable by applying it to generate instances for two different portfolios, one based on stochastic algorithms and other based on deterministic heuristics.
