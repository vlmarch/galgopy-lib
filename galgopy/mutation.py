import random
from abc import ABC, abstractmethod

from .objects import *


class AbstractMutation(ABC):
    def __init__(self, mutation_probability=0.01) -> None:
        super().__init__()
        self._mutation_probability = mutation_probability

    @abstractmethod
    def apply_mutation(self, chromosome):
        pass


class RandomMutation(AbstractMutation):
    def apply_mutation(self, chromosome):
        for i, g in enumerate(chromosome.genes_list):
            if random.random() <= self._mutation_probability:
                chromosome.genes_list[i] = Gene.generate_random_gene(
                    g.gene_type
                )
        return chromosome
