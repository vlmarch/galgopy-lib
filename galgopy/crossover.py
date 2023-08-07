# -*- coding: utf-8 -*-
"""Module with crossovers.

Module includes:
    AbstractCrossover
    OnePointCrossover
    MultipointCrossover

"""

import random
from abc import ABC, abstractmethod

from .genetypes import FloatType
from .objects import Chromosome, Gene, Population


class AbstractCrossover(ABC):
    """Abstract Crossover."""

    def __init__(self, proportionate_selection=True) -> None:
        """Crossover.

        Args:
            proportionate_selection (bool, optional): Mode of parents selection.
                True - proportional selection. False - random selection.
                Defaults to True.
        """
        self._proportionate_selection = proportionate_selection

    def _select_parents(self, parents: Population, count=2) -> tuple:
        """Parents selection for crossover.

        Args:
            parents (Population): Parent population.
            count (int, optional): Number of parents for crossower. Defaults to 2.

        Returns:
            tuple: Selected parents.
        """
        if self._proportionate_selection:
            weights = [p.proportional_fitness for p in parents]
            selected_parents = random.choices(parents, weights=weights, k=count)
        else:
            selected_parents = random.sample(parents, k=count)
        return tuple(selected_parents)

    @abstractmethod
    def generate_new_population(
        self, parents: Population, next_population_size: int
    ) -> Population:
        """Generating new population.

        Args:
            parents (Population): Parent population.
            next_population_size (int): The number of cromosomes in the new population.

        Returns:
            Population:  New population.
        """


class OnePointCrossover(AbstractCrossover):
    """One-point crossover"""

    def generate_new_population(
        self, parents: Population, next_population_size: int
    ) -> Population:
        new_population_list = []
        while len(new_population_list) < next_population_size:
            perent1, perent2 = self._select_parents(parents)
            cut_point = random.randint(1, len(perent1) - 1)
            child1 = Chromosome(perent1[:cut_point] + perent2[cut_point:])
            child2 = Chromosome(perent2[:cut_point] + perent1[cut_point:])
            new_population_list.append(child1)
            if len(new_population_list) == next_population_size:
                break
            new_population_list.append(child2)
        return Population(new_population_list)


class MultipointCrossover(AbstractCrossover):
    """Multi-point crossover"""

    def __init__(
        self,
        proportionate_selection=True,
        cut_points_count=2,
    ) -> None:
        """Multi-point crossover.

        Args:
            proportionate_selection (bool, optional): Mode of parents selection.
                True - proportional selection. False - random selection.
                Defaults to True.
            cut_points_count (int, optional): Number of cutting points. Defaults to 2.

        Raises:
            ValueError: Invalid number of cutting points.
        """
        super().__init__(proportionate_selection)
        if cut_points_count < 2:
            raise ValueError("The cut points should be 2 or more.")
        self._cut_points_count = cut_points_count

    def generate_new_population(
        self, parents: Population, next_population_size: int
    ) -> Population:
        new_population_list = []
        while len(new_population_list) < next_population_size:
            perent1, perent2 = self._select_parents(parents)

            cut_points = sorted(
                random.sample(range(len(perent1)), k=self._cut_points_count)
            )

            child1 = []
            child2 = []

            for i in range(len(cut_points) + 1):
                if i == 0:
                    child1 += perent2[: cut_points[i]]
                    child2 += perent1[: cut_points[i]]
                elif i == len(cut_points):
                    if i % 2:
                        child1 += perent1[cut_points[i - 1] :]
                        child2 += perent2[cut_points[i - 1] :]
                    else:
                        child1 += perent2[cut_points[i - 1] :]
                        child2 += perent1[cut_points[i - 1] :]
                elif i % 2:
                    child1 += perent1[cut_points[i - 1] : cut_points[i]]
                    child2 += perent2[cut_points[i - 1] : cut_points[i]]
                else:
                    child1 += perent2[cut_points[i - 1] : cut_points[i]]
                    child2 += perent1[cut_points[i - 1] : cut_points[i]]
            new_population_list.append(Chromosome(child1))
            if len(new_population_list) == next_population_size:
                break
            new_population_list.append(Chromosome(child2))
        return Population(new_population_list)


class UniformCrossover(AbstractCrossover):
    """Uniform crossover"""

    def generate_new_population(
        self, parents: Population, next_population_size: int
    ) -> Population:
        new_population_list = []
        while len(new_population_list) < next_population_size:
            perent1, perent2 = self._select_parents(parents)

            child1 = []
            child2 = []

            for gene1, gene2 in zip(perent1, perent2):
                chance = random.random()
                if chance < 0.5:
                    child1.append(gene1)
                    child2.append(gene2)
                else:
                    child1.append(gene2)
                    child2.append(gene1)
            new_population_list.append(Chromosome(child1))
            if len(new_population_list) == next_population_size:
                break
            new_population_list.append(Chromosome(child2))
        return Population(new_population_list)


class IntermediateRecombinationCrossover(AbstractCrossover):
    """Intermediate recombination crossover"""

    def __init__(self, proportionate_selection=True, a=0.5) -> None:
        """Intermediate recombination crossover.

        Args:
            proportionate_selection (bool, optional): Mode of parents selection.
                True - proportional selection. False - random selection.
                Defaults to True.
            a (float, optional): a value. Defaults to 0.5.

        Raises:
            ValueError: Invalid value of a. a should be 0 <= a <= 1
        """
        super().__init__(proportionate_selection)
        if not (0 <= a <= 1):
            raise ValueError("Invalid value of a. a should be 0 <= a <= 1")
        self._a = a

    def generate_new_population(
        self, parents: Population, next_population_size: int
    ) -> Population:
        if not (
            parents.chromosome_tmplt.types_of_class(FloatType)
            and parents.chromosome_tmplt.are_same_types()
        ):
            raise ValueError(
                "Incorrect population. All population chromosome genes should be FloatType type."
            )
        new_population_list = []
        while len(new_population_list) < next_population_size:
            perent1, perent2 = self._select_parents(parents)
            if self._a == 0.5:
                child = [
                    Gene(
                        (gene1.value + gene2.value) * self._a,
                        gene_type=gene1.gene_type,
                    )
                    for gene1, gene2 in zip(perent1, perent2)
                ]
                new_population_list.append(Chromosome(child))
            else:
                child1 = []
                child2 = []

                for gene1, gene2 in zip(perent1, perent2):
                    child1.append(
                        Gene(
                            gene1.value * self._a + gene2.value * (1 - self._a),
                            gene_type=gene1.gene_type,
                        )
                    )
                    child2.append(
                        Gene(
                            gene2.value * self._a + gene1.value * (1 - self._a),
                            gene_type=gene2.gene_type,
                        )
                    )

                new_population_list.append(Chromosome(child1))
                if len(new_population_list) == next_population_size:
                    break
                new_population_list.append(Chromosome(child2))
        return Population(new_population_list)
