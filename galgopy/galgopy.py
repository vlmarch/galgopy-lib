from .crossover import UniformCrossover
from .mutation import RandomMutation


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
