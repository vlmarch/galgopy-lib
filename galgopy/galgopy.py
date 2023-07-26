import random
from abc import ABC, abstractmethod

from .genetypes import *


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
                f"The given gene value ({value}) does not correspond to its type ({gene_type})."
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
            raise ValueError("Changing 'value' properties is not allowed.")
        self._value = value

    @property
    def gene_type(self):
        """Gene type."""
        return self._gene_type

    @gene_type.setter
    def gene_type(self, value):
        raise ValueError("Changing 'gene_type' properties is not allowed.")

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
        raise ValueError("Changing 'types_list' properties is not allowed.")


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
                "Invalid genes list. The list should contain only genes and it can't be empty."
            )
        self._genes_list = genes_list
        self._chromosome_tmplt = ChromosomeTemplate(
            [g.gene_type for g in genes_list]
        )
        self._fitness = 0
        self._proportional_fitness = 0

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
        """List of genes in the chromosome."""
        return self._genes_list

    @genes_list.setter
    def genes_list(self, value):
        raise ValueError("Changing 'genes_list' properties is not allowed.")

    @property
    def chromosome_tmplt(self):
        """Chromosome template."""
        return self._chromosome_tmplt

    @chromosome_tmplt.setter
    def chromosome_tmplt(self, value):
        raise ValueError(
            "Changing 'chromosome_tmplt' properties is not allowed."
        )

    @property
    def fitness(self):
        """The fitness value of chromosomes."""
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def proportional_fitness(self):
        """The proportional fitness value of chromosomes."""
        return self._proportional_fitness

    @proportional_fitness.setter
    def proportional_fitness(self, value):
        self._proportional_fitness = value

    @staticmethod
    def generate_random_chromosome(chromosome_tmplt: ChromosomeTemplate):
        """Creates a chromosome with random genes values based on a template.

        Args:
            chromosome_tmplt (ChromosomeTemplate): Chromosome template.

        Returns:
            Chromosome: Random chromosome.
        """
        chromosome = Chromosome(
            [Gene.generate_random_gene(t) for t in chromosome_tmplt.types_list]
        )
        return chromosome


class Population:
    """Population implementation."""

    def __init__(self, chromosome_list):
        """Chromosome population.

        Args:
            chromosome_list (list): Chromosome list.

        Raises:
            ValueError: Not all chromosomes in the given list have the same template.
        """
        if any(
            [
                c.chromosome_tmplt != chromosome_list[0].chromosome_tmplt
                for c in chromosome_list
            ]
        ):
            raise ValueError(
                "Not all chromosomes in the given list have the same template."
            )
        self._chromosome_list = chromosome_list
        self._fitness_mode = "maximize"

    def __str__(self) -> str:
        return "Population(\n    {}\n    )".format(
            "\n    ".join([str(c) for c in self._chromosome_list])
        )

    def __len__(self) -> int:
        return len(self._chromosome_list)

    @property
    def chromosome_list(self):
        """List of chromosomes included in the population."""
        return self._chromosome_list

    @chromosome_list.setter
    def chromosome_list(self, value):
        raise ValueError(
            "Changing 'chromosome_list' properties is not allowed."
        )

    def fitness(self, func, mode="maximize"):
        """Applies fitness function to the population.

        Args:
            func (function): Fitness function.
            mode (str, optional): Fitness mode. Options: "maximize" and
                "minimize". Defaults to "maximize".

        Raises:
            ValueError: Invalid mode.
        """
        if mode not in ["maximize", "minimize"]:
            raise ValueError(
                f"'{mode}' mode is not correct. Modes of choice: 'maximize' and 'minimize'."
            )
        self._fitness_mode = mode
        for chromosome in self._chromosome_list:
            chromosome.fitness = func(chromosome)
        self._chromosome_list.sort()
        if mode == "maximize":
            self._chromosome_list.reverse()

    def get_parents(self, parents_count=2):
        """Returns a list of the best parents.

        Args:
            parents_count (int, optional): The number of parents for the next
                generation. Defaults to 2.

        Raises:
            ValueError: Invalid number of parents.
        Returns:
            list: Selected parents.
        """
        if parents_count > len(self._chromosome_list):
            raise ValueError(
                f"The number of parents given ({parents_count}) is greater than the number of chromosomes ({len(self._chromosome_list)})."
            )
        elif parents_count < 1:
            raise ValueError("The number of parents should be greater than 0.")

        selected_parents = self._chromosome_list[:parents_count]

        fitness_min = min([p.fitness for p in selected_parents])
        fitness_sum = sum([p.fitness - fitness_min for p in selected_parents])

        for parent in selected_parents:
            if fitness_sum == 0:
                parent.proportional_fitness = 1 / parents_count
            elif self._fitness_mode == "maximize":
                parent.proportional_fitness = (
                    parent.fitness - fitness_min
                ) / fitness_sum
            else:  # "minimize"
                parent.proportional_fitness = (
                    1 - (parent.fitness - fitness_min) / fitness_sum
                ) / fitness_sum
        return selected_parents

    def apply_mutation(self, mutation):
        """Apply mutations for populations.

        Args:
            mutation: Mutation object that inherits class AbstractMutation.
        """
        for i, chromosome in enumerate(self._chromosome_list):
            self._chromosome_list[i] = mutation.apply_mutation(chromosome)

    @staticmethod
    def generate_random_population(
        population_size, chromosome_tmplt: ChromosomeTemplate
    ):
        """Creates a random population.

        Args:
            population_size (int): The number of cromosomes in the population.
            chromosome_tmplt (ChromosomeTemplate): Chromosome template.

        Returns:
            Population: New random poulation.
        """
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
            weights = [p.proportional_fitness for p in parents]
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


################################################################################


class GA:
    def __init__(
        self,
        population,
        fitness_func,
        fitness_mode="maximize",
        parents_count=2,
        crossover=UniformCrossover(),
        mutation=RandomMutation(),
        max_generations=100,
        expected_fitness=None,
    ) -> None:
        self._population = population
        self._fitness_func = fitness_func
        self._fitness_mode = fitness_mode
        self._parents_count = parents_count
        self._crossover = crossover
        self._mutation = mutation
        self._max_generations = max_generations
        self._expected_fitness = expected_fitness

    def start(self):
        temp_fitnes = None
        generation = 1
        while not (
            (self._expected_fitness == temp_fitnes != None)
            or (generation == self._max_generations)
        ):
            self._population.fitness(
                self._fitness_func, mode=self._fitness_mode
            )
            parents = self._population.get_parents(self._parents_count)

            temp_fitnes = parents[0].fitness
            print(
                f"Generation {generation}: {parents[0]}. Fitness: {parents[0].fitness}."
            )

            population = self._crossover.generate_new_population(
                parents, len(self._population)
            )
            population.apply_mutation(self._mutation)
            self._population = population
            generation += 1
