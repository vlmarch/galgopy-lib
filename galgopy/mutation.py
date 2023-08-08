# -*- coding: utf-8 -*-
"""Module with mutation.

Module includes:
    AbstractMutation
    RandomMutation
    SwapMutation

To Do:
    Add Scramble Mutation
    Add Inversion Mutation

"""

import random
from abc import ABC, abstractmethod

from galgopy.objects import Chromosome

from .objects import Chromosome, Gene


class AbstractMutation(ABC):
    """Abstract Mutation."""

    def __init__(self, mutation_probability=0.01) -> None:
        """Mutation.

        Args:
            mutation_probability (float, optional): Mutation probability. Defaults to 0.01.
        """
        self._mutation_probability = mutation_probability

    @abstractmethod
    def apply_mutation(self, chromosome: Chromosome) -> Chromosome:
        """Apply chromosome mutations.

        Args:
            chromosome (Chromosome): Chromosome.

        Returns:
            Chromosome: Mutated chromosome.
        """


class RandomMutation(AbstractMutation):
    """Random mutation."""

    def apply_mutation(self, chromosome):
        new_genes_list = chromosome.genes_list.copy()
        for i, gene in enumerate(chromosome.genes_list):
            if random.random() <= self._mutation_probability:
                new_genes_list[i] = Gene.generate_random_gene(gene.gene_type)
        return Chromosome(new_genes_list)


class SwapMutation(AbstractMutation):
    """Swap mutation."""

    def apply_mutation(self, chromosome: Chromosome) -> Chromosome:
        """Apply swap mutation.

        Args:
            chromosome (Chromosome): Chromosome.

        Raises:
            ValueError: Impossible to apply swap mutation.

        Returns:
            Chromosome: Mutated chromosome.
        """
        if not chromosome.chromosome_tmplt.are_same_types():
            raise ValueError(
                "All genes in a chromosome should be the same. On this chromosome it is impossible to apply Swap mutation."
            )
        if len(chromosome) < 2:
            raise ValueError(
                "It is impossible to use Swap mutation for this chromosome. The chromosome should have more than 2 genes."
            )
        new_genes_list = chromosome.genes_list.copy()
        if random.random() <= self._mutation_probability:
            points = random.sample(range(len(chromosome)), k=2)
            new_genes_list[points[0]], new_genes_list[points[1]] = (
                chromosome[points[1]],
                chromosome[points[0]],
            )
        return Chromosome(new_genes_list)
