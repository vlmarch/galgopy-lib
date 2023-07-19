import random
from abc import ABC, abstractmethod

import gtypes

################################################################################


class Gene:
    def __init__(self, value=0, gene_type=gtypes.BinaryType()) -> None:
        if not gene_type.validate(value):
            raise ValueError()
        self._value = value
        self._gene_type = gene_type

    def __str__(self) -> str:
        return f"Gene({self._value})"

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self._gene_type.validate(value):
            raise ValueError()
        self._value = value

    @property
    def gene_type(self):
        return self._gene_type

    @gene_type.setter
    def gene_type(self, value):
        raise ValueError()

    @staticmethod
    def generate_random_gene(gene_type=gtypes.BinaryType()):
        return Gene(gene_type.get_random_val(), gene_type)


class ChromosomeTemplate:
    def __init__(self, types_list=[gtypes.BinaryType() for i in range(8)]):
        self._types_list = types_list

    def __str__(self) -> str:
        return f"CT({' '.join([str(t) for t in self._types_list])})"

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self)) and self._types_list == __o.types_list
        )

    @property
    def types_list(self):
        return self._types_list

    @types_list.setter
    def types_list(self, value):
        raise ValueError()


class Chromosome:
    def __init__(self, genes_list=[Gene() for i in range(8)]):
        if any([g.gene_type != genes_list[0].gene_type for g in genes_list]):
            raise ValueError
        elif not genes_list:
            raise ValueError("Invalid genes list")
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


class Crossover(ABC):
    def __init__(
        self, parents, next_population_size, proportionate_selection=True
    ) -> None:
        self._parents = parents
        self._next_population_size = next_population_size
        self._proportionate_selection = proportionate_selection

    def _select_parents(self):
        if self._proportionate_selection:
            weights = [p.fitness for p in self._parents]
            if sum(weights) == 0:
                weights = [1] * len(weights)
            selected_parents = random.choices(
                self._parents, weights=weights, k=2
            )
        else:
            selected_parents = random.sample(self._parents, k=2)
        return tuple(selected_parents)

    @abstractmethod
    def generate_new_population(self):
        pass


class OnePointCrossover(Crossover):
    def generate_new_population(self):
        new_population_list = []
        for i in range(round(self._next_population_size / 2)):
            p1, p2 = self._select_parents()
            cut_point = random.randint(1, len(p1) - 1)
            c1 = Chromosome(p1[:cut_point] + p2[cut_point:])
            c2 = Chromosome(p2[:cut_point] + p1[cut_point:])
            new_population_list.append(c1)
            new_population_list.append(c2)
            print(list(range(1, len(p1))))
        return Population(new_population_list)


class MultipointCrossover(Crossover):
    def __init__(
        self,
        parents,
        next_population_size,
        proportionate_selection=True,
        cut_points_count=3,
    ) -> None:
        super().__init__(parents, next_population_size, proportionate_selection)
        self._cut_points_count = cut_points_count

    def generate_new_population(self):
        new_population_list = []
        for i in range(round(self._next_population_size / 2)):
            p1, p2 = self._select_parents()

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


# class UniformCrossover(Crossover):
#     def __init__(self) -> None:
#         super().__init__()

#     def get_parents(self):
#         pass

################################################################################


class Mutation(ABC):
    def __init__(self, population, mutation_probability=0.01) -> None:
        super().__init__()
        self._population = population
        self._mutation_probability = mutation_probability

    @abstractmethod
    def apply_mutations(self):
        pass


class RandomMutation(Mutation):
    def apply_mutations(self):
        for c in self._population.chromosome_list:
            for i, g in enumerate(c.genes_list):
                if random.random() <= self._mutation_probability:
                    c.genes_list[i] = Gene.generate_random_gene(g.gene_type)
        return self._population


################################################################################


def fitness_calculation(chromosome):
    return sum(
        [
            g.value == l
            for g, l in zip(chromosome.genes_list, ["v", "l", "a", "d"])
        ]
    )


################################################################################


if __name__ == "__main__":
    chromosome_len = 5
    init_population_size = 10
    parents_count = 2

    ct = ChromosomeTemplate([gtypes.StrType("lowercase")] * 4)

    population = Population.generate_random_population(init_population_size, ct)
    fitness = 0

    while fitness != 4:
        population.fitness(fitness_calculation)
        parents = population.get_parents(parents_count)

        fitness = parents[0].fitness
        print(parents[0])

        crossover = MultipointCrossover(parents, init_population_size)
        population = crossover.generate_new_population()

        mutation = RandomMutation(population, mutation_probability=0.1)
        population = mutation.apply_mutations()
