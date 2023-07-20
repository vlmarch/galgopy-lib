import random
from abc import ABC, abstractmethod

from .gtypes import *


class Gene:
    """Gene implementation."""

    def __init__(self, value=0, gene_type=BinaryType()) -> None:
        """Gene - one of the elements of the chromosome.

        Args:
            value (int, optional): The value the gene takes. Defaults to 0.
            gene_type (GeneType(), optional): Gene type. Defaults to BinaryType().

        Raises:
            ValueError: The value of a gene does not correspond to its type.
        """
        if not gene_type.validate(value):
            raise ValueError(
                "The given gene value does not correspond to its type."
            )
        self._value = value
        self._gene_type = gene_type

    def __str__(self) -> str:
        return f"Gene({self._value})"

    @property
    def value(self):
        """The value of the gene."""
        return self._value

    @value.setter
    def value(self, value):
        if not self._gene_type.validate(value):
            raise ValueError()
        self._value = value

    @property
    def gene_type(self):
        """Gene type."""
        return self._gene_type

    @gene_type.setter
    def gene_type(self, value):
        raise ValueError()

    @staticmethod
    def generate_random_gene(gene_type=BinaryType()):
        """Generates a gene with a random value.

        Args:
            gene_type (GeneType(), optional): Gene type. Defaults to BinaryType().

        Returns:
            Gene(): Gene with random value.
        """
        return Gene(gene_type.get_random_val(), gene_type)


class ChromosomeTemplate:
    """Chromosome template implementation."""

    def __init__(self, types_list=[BinaryType() for i in range(8)]):
        """Chromosome template - chromosomes pattern consist of a list of gene types.

        Args:
            types_list (list, optional): List of gene types included in the
                chromosome. Defaults to [BinaryType() for i in range(8)].
        """
        self._types_list = types_list

    def __str__(self) -> str:
        return f"CT({' '.join([str(t) for t in self._types_list])})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self)) and self._types_list == __o.types_list
        )

    @property
    def types_list(self):
        """List of gene types included in the chromosome."""
        return self._types_list

    @types_list.setter
    def types_list(self, value):
        raise ValueError()


class Chromosome:
    """Chromosome implementation."""

    def __init__(self, genes_list=[Gene() for i in range(8)]):
        """Chromosome - is composed of genes.

        Args:
            genes_list (list, optional): List of genes contained in the
                chromosome. Defaults to [Gene() for i in range(8)].

        Raises:
            ValueError: Invalid list of gens.
        """
        if not genes_list or any([not isinstance(g, Gene) for g in genes_list]):
            raise ValueError(
                "Invalid list of gens. The list should contain only genes."
            )
        self._genes_list = genes_list
        self._chromosome_tmplt = ChromosomeTemplate(
            [g.gene_type for g in genes_list]
        )
        self._fitness = 0

    def __str__(self) -> str:
        return (
            f"Chromosome({' '.join([str(t.value) for t in self._genes_list])})"
        )

    def __len__(self) -> int:
        return len(self._genes_list)

    def __lt__(self, __o):
        return self._fitness < __o.fitness

    def __getitem__(self, i):
        return self._genes_list[i]

    @property
    def genes_list(self):
        return self._genes_list

    @genes_list.setter
    def genes_list(self, value):
        raise ValueError()

    @property
    def chromosome_tmplt(self):
        return self._chromosome_tmplt

    @chromosome_tmplt.setter
    def chromosome_tmplt(self, value):
        raise ValueError()

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @staticmethod
    def generate_random_chromosome(chromosome_tmplt: ChromosomeTemplate):
        chromosome = Chromosome(
            [Gene.generate_random_gene(t) for t in chromosome_tmplt.types_list]
        )
        return chromosome


class Population:
    def __init__(self, chromosome_list):
        if any(
            [
                c.chromosome_tmplt != chromosome_list[0].chromosome_tmplt
                for c in chromosome_list
            ]
        ):
            raise ValueError
        self._chromosome_list = chromosome_list
        self._index = 0

    def __str__(self) -> str:
        return "Population(\n    {}\n    )".format(
            "\n    ".join([str(c) for c in self._chromosome_list])
        )

    def __len__(self) -> int:
        return len(self._chromosome_list)

    @property
    def chromosome_list(self):
        return self._chromosome_list

    @chromosome_list.setter
    def chromosome_list(self, value):
        raise ValueError()

    def fitness(self, func, mode="maximize"):
        for c in self._chromosome_list:
            c.fitness = func(c)
        self._chromosome_list.sort()
        if mode == "maximize":
            self._chromosome_list.reverse()

    def get_parents(self, parents_count=2):
        if parents_count > len(self._chromosome_list):
            raise ValueError()
        elif parents_count < 1:
            raise ValueError()
        return self._chromosome_list[:parents_count]

    def apply_mutation(self, mutation):
        for i, chromosome in enumerate(self._chromosome_list):
            self._chromosome_list[i] = mutation._apply_mutation(chromosome)

    @staticmethod
    def generate_random_population(
        population_size, chromosome_tmplt: ChromosomeTemplate
    ):
        return Population(
            [
                Chromosome.generate_random_chromosome(chromosome_tmplt)
                for _ in range(population_size)
            ]
        )


################################################################################


class AbstractCrossover(ABC):
    def __init__(self, proportionate_selection=True) -> None:
        self._proportionate_selection = proportionate_selection

    def _select_parents(self, parents, count=2):
        if self._proportionate_selection:
            weights = [p.fitness for p in parents]
            if sum(weights) == 0:
                weights = [1] * len(weights)
            selected_parents = random.choices(parents, weights=weights, k=count)
        else:
            selected_parents = random.sample(parents, k=count)
        return tuple(selected_parents)

    @abstractmethod
    def generate_new_population(self, parents, next_population_size):
        pass


class OnePointCrossover(AbstractCrossover):
    def generate_new_population(self, parents, next_population_size):
        new_population_list = []
        for _ in range(round(next_population_size / 2)):
            p1, p2 = self._select_parents(parents)
            cut_point = random.randint(1, len(p1) - 1)
            c1 = Chromosome(p1[:cut_point] + p2[cut_point:])
            c2 = Chromosome(p2[:cut_point] + p1[cut_point:])
            new_population_list.append(c1)
            new_population_list.append(c2)
            print(list(range(1, len(p1))))
        return Population(new_population_list)


class MultipointCrossover(AbstractCrossover):
    def __init__(
        self,
        proportionate_selection=True,
        cut_points_count=3,
    ) -> None:
        super().__init__(proportionate_selection)
        self._cut_points_count = cut_points_count

    def generate_new_population(self, parents, next_population_size):
        new_population_list = []
        for _ in range(round(next_population_size / 2)):
            p1, p2 = self._select_parents(parents)

            cut_points = sorted(
                random.sample(range(1, len(p1)), k=self._cut_points_count)
            )

            c1 = []
            c2 = []

            for i in range(len(cut_points) + 1):
                if i == 0:
                    c1 += p2[: cut_points[i]]
                    c2 += p1[: cut_points[i]]
                elif i == len(cut_points):
                    if i % 2:
                        c1 += p1[cut_points[i - 1] :]
                        c2 += p2[cut_points[i - 1] :]
                    else:
                        c1 += p2[cut_points[i - 1] :]
                        c2 += p1[cut_points[i - 1] :]
                elif i % 2:
                    c1 += p1[cut_points[i - 1] : cut_points[i]]
                    c2 += p2[cut_points[i - 1] : cut_points[i]]
                else:
                    c1 += p2[cut_points[i - 1] : cut_points[i]]
                    c2 += p1[cut_points[i - 1] : cut_points[i]]
            new_population_list.append(Chromosome(c1))
            new_population_list.append(Chromosome(c2))
        return Population(new_population_list)


class UniformCrossover(AbstractCrossover):
    def generate_new_population(self, parents, next_population_size):
        new_population_list = []
        for _ in range(round(next_population_size / 2)):
            p1, p2 = self._select_parents(parents)

            c1 = []
            c2 = []

            for g1, g2 in zip(p1, p2):
                chance = random.random()
                if chance < 0.5:
                    c1.append(g1)
                    c2.append(g2)
                else:
                    c1.append(g2)
                    c2.append(g1)
            new_population_list.append(Chromosome(c1))
            new_population_list.append(Chromosome(c2))
        return Population(new_population_list)


################################################################################


class AbstractMutation(ABC):
    def __init__(self, mutation_probability=0.01) -> None:
        super().__init__()
        self._mutation_probability = mutation_probability

    @abstractmethod
    def _apply_mutation(self, chromosome):
        pass


class RandomMutation(AbstractMutation):
    def _apply_mutation(self, chromosome):
        for i, g in enumerate(chromosome.genes_list):
            if random.random() <= self._mutation_probability:
                chromosome.genes_list[i] = Gene.generate_random_gene(
                    g.gene_type
                )
        return chromosome


################################################################################


class GA:
    def __init__(
        self,
        population,
        fitness_func,
        parents_count=2,
        crossover=UniformCrossover(),
        mutation=RandomMutation(),
        max_generations=10000,
        expected_fitness=None,
    ) -> None:
        self._population = population
        self._fitness_func = fitness_func
        self._parents_count = parents_count
        self._crossover = crossover
        self._mutation = mutation
        self._max_generations = max_generations
        self._expected_fitness = expected_fitness

    def start(self):
        temp_fitnes = 0
        generation = 1
        while not (
            (self._expected_fitness == temp_fitnes)
            or (generation == self._max_generations)
        ):
            self._population.fitness(self._fitness_func)
            parents = self._population.get_parents(self._parents_count)

            temp_fitnes = parents[0].fitness
            print(f"Generation {generation} : {parents[0]}")

            population = self._crossover.generate_new_population(
                parents, len(self._population)
            )
            population.apply_mutation(self._mutation)
            self._population = population
            generation += 1
