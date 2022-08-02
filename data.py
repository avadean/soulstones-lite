from numpy import arange, exp


BIRTH_PARAM = 0.04 # Per cent of able population to have children.

INIT_CHANCE_DEATH = 0.0001  #0.001
EXPO_CHANCE_DEATH = 0.078   #0.051
MAX_AGE = 150

deathProbs = INIT_CHANCE_DEATH * exp(EXPO_CHANCE_DEATH * arange(MAX_AGE + 50)) # +50 to be safe.

MIN_CHILD_AGE = 18
MAX_CHILD_AGE = 45

GOOD_BALANCE = 8.0
PROB_PREFACTOR = 1.0


def createAges(rng, num: int, minAge: int = 0, maxAge: int = 100):
    return rng.integers(low=minAge, high=maxAge, size=num, dtype=int)
