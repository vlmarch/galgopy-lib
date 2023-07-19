import random

import gtypes


class ChromosomeTemplate:
    def __init__(self, types_list=[gtypes.BinaryType()] * 8) -> None:
        self.genes_count = len(types_list)
        self.types_list = types_list

    def __eq__(self, __o: object) -> bool:
        return all([a == b for a, b in zip(self.types_list, __o.types_list)])

    def check_chromosome(self, n):
        return all(
            a == b
            for a, b in zip(n.chromosome_tmplt.types_list, self.types_list)
        )


class Chromosome:
    def __init__(self, val_list, chromosome_tmplt: ChromosomeTemplate) -> None:
        if len(val_list) != len(chromosome_tmplt.types_list):
            raise ValueError()
        if any(
            [
                not t.validate(v)
                for v, t in zip(val_list, chromosome_tmplt.types_list)
            ]
        ):
            raise ValueError()
        self.val_list = val_list
        self.chromosome_tmplt = chromosome_tmplt
        self.fitness = 0
        self.probability_of_choosing = 0

    def __str__(self) -> str:
        return "Chromosome({})".format(
            " ".join([str(g) for g in self.val_list])
        )

    def __eq__(self, __o: object) -> bool:
        return (
            self.chromosome_tmplt == __o.chromosome_tmplt
            and self.val_list == __o.val_list
        )

    def __lt__(self, __o):
        return self.fitness < __o.fitness

    @staticmethod
    def generate_random_chromosome(chromosome_tmplt: ChromosomeTemplate):
        return Chromosome(
            [t.get_random_val() for t in chromosome_tmplt.types_list],
            chromosome_tmplt,
        )


class Population:
    def __init__(
        self, population, chromosome_tmplt: ChromosomeTemplate
    ) -> None:
        if any(
            [not chromosome_tmplt.check_chromosome(ch) for ch in population]
        ):
            raise ValueError()

        self.population_count = len(population)
        self.population = population
        self.chromosome_tmplt = chromosome_tmplt

    def __str__(self) -> str:
        return "Population(\n    {}\n    )".format(
            "\n    ".join([str(c) for c in self.population])
        )

    def fitness(self, func, mode="maximize"):
        for chromosome in self.population:
            chromosome.fitness = func(chromosome)
        self.population.sort()
        if mode == "maximize":
            self.population.reverse()

    def get_parents(self, parents_count=2):
        if parents_count > self.population_count:
            raise ValueError()
        elif parents_count < 1:
            raise ValueError()
        return self.population[:parents_count]

    @staticmethod
    def generate_random_population(
        population_count, chromosome_tmplt: ChromosomeTemplate
    ):
        population = [
            Chromosome.generate_random_chromosome(chromosome_tmplt)
            for i in range(population_count)
        ]
        return Population(population, chromosome_tmplt)


################################################################################


def fitness_calculation(chromosome):
    return sum(chromosome.val_list)


################################################################################


class GAlgo:
    """Genetic Algorithm (GA)"""

    def __init__(self) -> None:
        pass


################################################################################

if __name__ == "__main__":
    chromosome_len = 5
    init_population_size = 5
    parents_count = 2

    ct = ChromosomeTemplate()

    population = Population.generate_random_population(init_population_size, ct)
    fitness_value = 0

    while fitness_value != 8:
        population.fitness(fitness_calculation)

        parents = population.get_parents(parents_count)
        fitness_value = parents[0].fitness
        print(parents[0])
        cross = crossover.OnePointCrossover(parents, 10)
        population = cross.get_next_population()

        m = mutation.FlipMutation(population)
        population = m.apply_mutation()


################################################################################
