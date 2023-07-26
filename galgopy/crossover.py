import random
from abc import ABC, abstractmethod

from .objects import Chromosome, Population


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
