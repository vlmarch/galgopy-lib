import random

import gtypes

################################################################################


class ChromosomeTemplate:
    def __init__(self, types_list=[gtypes.BinaryType() for i in range(8)]):
        self._types_list = types_list
        self._index = 0

    def __str__(self) -> str:
        # WIP
        return "ChromosomeTemplate()"

    def __setitem__(self, i, data):
        # WIP
        raise ValueError()

    def __getitem__(self, i):
        return self._types_list[i]

    def __len__(self):
        return len(self._types_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._types_list):
            item = self._types_list[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration

    def __eq__(self, __o: object) -> bool:
        return self._types_list == __o.types_list

    @property
    def types_list(self):
        return self._types_list

    @types_list.setter
    def types_list(self, value):
        raise ValueError()


# print(ChromosomeTemplate())
# print(list(ChromosomeTemplate()))


################################################################################


class Gene:
    def __init__(self, value=0, gene_type=gtypes.BinaryType()) -> None:
        if not gene_type.validate(value):
            raise ValueError()
        self._value = value
        self._gene_type = gene_type

    def __str__(self) -> str:
        return "Gene({})".format(str(self._value))

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self))
            and self._value == __o.value
            and self._gene_type == __o.gene_type
        )

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
    def generate_random_gene(gene_type):
        return Gene(gene_type.get_random_val(), gene_type)


class Chromosome:
    def __init__(self, genes_list=[Gene() for i in range(8)]):
        if any([g.gene_type != genes_list[0].gene_type for g in genes_list]):
            raise ValueError
        self._genes_list = genes_list
        print(genes_list)
        self._chromosome_tmplt = ChromosomeTemplate(
            [g.gene_type for g in genes_list]
        )
        self._index = 0
        self._fitness = 0
        self._probability_of_choosing = 0

    def __str__(self) -> str:
        return f"Chromosome({' '.join([str(g.value) for g in self])})"

    def __setitem__(self, i, data):
        if self._genes_list[i].gene_type == data.gene_type:
            self._genes_list[i] = data
        else:
            raise ValueError

    def __getitem__(self, i):
        return self._genes_list[i]

    def __len__(self):
        return len(self._genes_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._genes_list):
            item = self._genes_list[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration

    def __eq__(self, __o: object) -> bool:
        return (
            isinstance(__o, type(self)) and self._genes_list == __o.genes_list
        )

    def __lt__(self, __o):
        return self._fitness < __o.fitness

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

    @staticmethod
    def generate_random_chromosome(chromosome_tmplt: ChromosomeTemplate):
        print(chromosome_tmplt)
        print("-------")
        chromosome = Chromosome(
            [Gene.generate_random_gene(t) for t in chromosome_tmplt]
        )
        return chromosome


################################################################################


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
            "\n    ".join([str(c) for c in self])
        )

    def __setitem__(self, i, data):
        self._chromosome_list[i] = data

    def __getitem__(self, i):
        return self._chromosome_list[i]

    def __len__(self):
        return len(self._chromosome_list)

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._chromosome_list):
            item = self._chromosome_list[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration

    def __eq__(self, __o: object) -> bool:
        return self._chromosome_list == __o.chromosome_list

    @property
    def chromosome_list(self):
        return self._chromosome_list

    @chromosome_list.setter
    def chromosome_list(self, value):
        raise ValueError()

    @staticmethod
    def generate_random_population(
        population_count, chromosome_tmplt: ChromosomeTemplate
    ):
        population = [
            Chromosome.generate_random_chromosome(chromosome_tmplt)
            for _ in range(population_count)
        ]
        print(population)
        return Population(population)


################################################################################


if __name__ == "__main__":
    chromosome_len = 5
    init_population_size = 5
    parents_count = 2

    ct = ChromosomeTemplate()

    # c = Chromosome.generate_random_chromosome(ChromosomeTemplate())

    # print(c)

    population = Population.generate_random_population(init_population_size, ct)
