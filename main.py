from collections import Counter
from numpy.random import default_rng
from cProfile import Profile
from pstats import Stats, SortKey

from data import createAges, MAX_AGE
from inout import writeInit, writeSummary
from population import Population


def main(rng, years: int = 100, pop: int = None, magic: Counter = None):
    assert isinstance(years, int)
    assert years > 0, 'Need to run for a non-zero number of years.'

    if magic is None:
        magic = Counter()
    else:
        assert isinstance(magic, Counter)
        assert 'null' not in magic, 'Do not define nulls in magic counter.'

    if pop is None:
        pop = sum(magic.values())
    else:
        assert isinstance(pop, int)

    if pop == 0:
        print('No population to simulate.')
        exit(1)
    else:
        assert pop >= sum(magic.values())

    souls = {age: Counter() for age in range(MAX_AGE)}

    # Nulls.
    for age, numOfAge in Counter(createAges(rng, pop - sum(magic.values()))).items():
        souls[age]['null'] += numOfAge

    # Magic.
    for soul, numOfSoul in magic.items():
        for age, numOfAge in Counter(createAges(rng, numOfSoul)).items():
            souls[age][soul] += numOfAge

    population = Population(souls)

    writeInit(population)

    for year in range(years):

        # Age up the population.
        population.ageUp()

        # Some people must die!
        population.deaths()

        # Stop if the population has hit zero.
        if population.getPop() == 0:
            break

        # Add new children.
        population.children(year)

        print(f'ending year {year} with pop {population.getPop()}')  # ... {persons}')

        #writeSummary(souls=population.getTotal(sort=True), index=year)

    writeSummary(souls=population.getTotal(sort=True), index=years)


if __name__ == '__main__':
    RNG = default_rng(seed=None)

    with Profile() as pr:
        main(rng=RNG, years=200, pop=500_000)
        '''magic=Counter({'water': 200_000,
                            'fire': 200_000,
                            'earth': 100_000,
                            'wind': 100_000,
                            'light': 40_000,
                            'dark': 20_000,
                            'stone': 10_000,
                            'metal': 10_000,
                            'flying': 10_000,
                            'ice': 10_000,
                            'lightning': 4_000,
                            'poison': 4_000,
                            'ghost': 4_000,
                            'psychic': 4_000,
                            'nuclear': 4_000,
                            'gravity': 4_000,
                            'life': 400,
                            'death': 400}))'''

    stats = Stats(pr)
    stats.sort_stats(SortKey.TIME)
    stats.print_stats()
    stats.dump_stats('timeProfiling.dat')
