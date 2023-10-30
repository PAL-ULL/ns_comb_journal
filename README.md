# Synthesising diverse and discriminatory sets of instances in combinatorial domains using novelty search

## Authors:

- Alejandro Marrero - amarrerd@ull.edu.es
- Eduardo Segredo - esegredo@ull.edu.es
- Coromoto León - cleon@ull.edu.es
- Emma Hart - e.hart@napier.ac.uk

## Abstract:
Gathering sufficient instance data to either train algorithm-selection models or understand algorithm footprints within an instance space can be challenging. We propose an approach to generating synthetic instances that are tailored to perform well with respect to a target algorithm belonging to a predefined portfolio but also diverse with respect to their features. Our approach uses a novelty search algorithm with a linearly weighted fitness function that balances novelty and performance, to generate a large set of diverse and discriminatory instances in a single run of the algorithm. We consider two definitions of novelty: (1) with respect to discriminatory performance within a portfolio of solvers; (2) with respect to the features of the evolved instances. We evaluate the proposed method with respect to its ability to generate diverse and discriminatory instances in two domains (knapsack and bin-packing), comparing to another well-known quality diversity method, Multi-dimensional Archive of Phenotypic Elites (MAP-Elites) and an evolutionary algorithm that only evolves for discriminatory behaviour. The results demonstrate that the proposal outperforms its competitors in terms of coverage of the space and its ability to generate instances that are diverse regarding the relative size of the ``performance gap'' between the target solver and the remaining solvers in the portfolio. Moreover, for the knapsack domain, we also show that we are able to generate novel instances in regions of an instance space not covered by existing benchmarks using a portfolio of state-of-the-art solvers. Finally, we demonstrate that the method is robust to different portfolios of solvers (stochastic approaches, deterministic heuristics and state-of-the-art methods), thereby providing further evidence of its generality.

## Source Code

The source code for all the algorithms is available through DIGNEA [here](https://github.com/DIGNEA/dignea).