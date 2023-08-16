# -*- coding: utf-8 -*-
"""Modul with implementation of genetic algorithm.

Module includes:
    GA

"""

from .crossover import AbstractCrossover, UniformCrossover
from .mutation import AbstractMutation, RandomMutation
from .objects import Chromosome, Population


class GA:
    """GA - Genetic algorithm."""

    def __init__(
        self,
        initial_population: Population,
        fitness_func,
        fitness_mode: str = "maximize",
        parents_count: int = 2,
        crossover: AbstractCrossover = UniformCrossover(),
        mutation: AbstractMutation = RandomMutation(),
        next_population_size: int = None,
    ) -> None:
        """GA - Genetic algorithm.

        Args:
            initial_population (Population): Initial population.
            fitness_func (_type_): Fitness function.
            fitness_mode (str, optional): itness mode. Options: "maximize" and
                "minimize". Defaults to "maximize".
            parents_count (int, optional): The number of parents for the next
                generation. Defaults to 2.
            crossover (AbstractCrossover, optional): Crossower for use in a
                genetic algorithm. Defaults to UniformCrossover().
            mutation (AbstractMutation, optional): Mutation for use in a
                genetic algorithm. Defaults to RandomMutation().
            next_population_size (int, optional): The number of cromosomes in
                the new population. None - gave the same amount as in the
                initial population. Defaults to None.
        """
        self._population = initial_population
        self._fitness_func = fitness_func
        self._fitness_mode = fitness_mode
        self._parents_count = parents_count
        self._crossover = crossover
        self._mutation = mutation
        self._next_population_size = next_population_size

        self._generation = 0
        self._best_solution = None
        self._best_fitness = None
        self._generation_best_solution = None
        self._generation_best_fitness = None
        self._generation_worst_solution = None
        self._generation_worst_fitness = None

        self._fitness()

    def __str__(self) -> str:
        return f"GA( generation={self._generation} )"

    def __next__(self) -> dict:
        self._generate_next()
        data = {
            "Generation": self._generation,
            "Best solution": self._best_solution,
            "Best fitness": self._best_fitness,
            "Generation best solution": self._generation_best_solution,
            "Generation best fitness": self._generation_best_fitness,
            "Generation worst solution": self._generation_worst_solution,
            "Generation worst fitness": self._generation_worst_fitness,
        }
        return data

    def __iter__(self):
        return self

    def _update_best_solution(self, chromosome: Chromosome):
        if (
            self._best_fitness is None
            or (
                chromosome.fitness > self._best_fitness
                and self._fitness_mode == "maximize"
            )
            or (
                chromosome.fitness < self._best_fitness
                and self._fitness_mode == "minimize"
            )
        ):
            self._best_solution = chromosome
            self._best_fitness = chromosome.fitness

    def _fitness(self):
        self._population.fitness(
            func=self._fitness_func, mode=self._fitness_mode
        )

        self._update_best_solution(self._population[0])
        self._generation_best_solution = self._population[0]
        self._generation_best_fitness = self._population[0].fitness
        self._generation_worst_solution = self._population[-1]
        self._generation_worst_fitness = self._population[-1].fitness

    def _generate_next(self):
        parents = self._population.get_parents(
            parents_count=self._parents_count
        )

        population = self._crossover.generate_new_population(
            parents=parents,
            next_population_size=len(self._population)
            if not self._next_population_size
            else self._next_population_size,
        )

        population.apply_mutation(mutation=self._mutation)
        self._population = population
        self._generation += 1
        self._fitness()

    def run(self, generations: int = 100, expected_fitness: float = None):
        """Runs a genetic algorithm.

        Args:
            generations (int, optional): Number of generations to be generated.
                Defaults to 100.
            expected_fitness (float, optional): Expected fitness value.
                None - for the generation of the total number of generations.
                Defaults to None.
        """
        for _ in range(generations):
            if expected_fitness == self._best_fitness:
                return
            self._generate_next()
