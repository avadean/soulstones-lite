from collections import Counter
from numpy import asarray, ceil
from numpy.random import choice
from random import choices

from data import deathProbs, BIRTH_PARAM, MAX_AGE, MIN_CHILD_AGE, MAX_CHILD_AGE
from soul import getSoul, processNulls, soulTable


class Population:
    def __init__(self, souls: dict = None):
        self.souls = {}

        self._zeroSouls()
        self.addSouls(souls)

    def __str__(self):
        return '\n'.join([f'{soul:>12} : {num:<9}' for soul, num in self.getTotal().items()])

    def _zeroSouls(self):
        self.souls = {age: Counter() for age in range(MAX_AGE)}

    def addSouls(self, soulsDict: dict = None):
        for age, souls in soulsDict.items():
            self.souls[age] += souls

    def addChildren(self, souls: Counter = None):
        try:
            self.souls[0] += souls
        except KeyError:
            self.souls[0] = souls

    def ageUp(self):
        self.souls = {age + 1: counter for age, counter in self.souls.items()}

    def children(self, year):
        ables = Counter()

        for age in range(MIN_CHILD_AGE, MAX_CHILD_AGE):
            ables.update(self.souls[age])

        souls, nums = list(ables.keys()), asarray(list(ables.values()), dtype=float)

        numAble = sum(nums)

        if numAble > 1:
            numChildren = int(ceil(BIRTH_PARAM * numAble))

            #parents = choices(ables, k=min(2 * numChildren, numAble))  # 2 * is for a mother and a father.

            parents = choice(souls,
                             size=min(2 * numChildren, numAble),  # 2 * is for a mother and a father.
                             p=nums / numAble)  # / numAble to normalise to probabilities.

            children = Counter(getSoul(motherSoul, fatherSoul, year)
                               for motherSoul, fatherSoul in zip(parents[:len(parents)//2],
                                                                 parents[len(parents)//2:]))

            if children['null'] > 0:
                # Turn nulls into randomised.
                children.update(processNulls(children.pop('null'), self.getTotal(sort=False)))

            self.addChildren(children)

    def deaths(self):
        for age in list(self.souls.keys()):

            # If prob. of dying >= 1 then just delete every person of that age and move on.
            if deathProbs[age] >= 1.0:
                self.souls.pop(age, None)
                continue

            # Not a great approximation for low population (which is fine).
            numToDie = int(ceil(sum(self.souls[age].values()) * deathProbs[age]))

            if numToDie > 0:
                self.souls[age].subtract(Counter(choices(list(self.souls[age].keys()),
                                                         weights=list(self.souls[age].values()),
                                                         k=numToDie)))

    def getPop(self):
        return sum(sum(souls.values()) for souls in self.souls.values())

    def getTotal(self, sort=False):
        total = Counter()

        for souls in self.souls.values():
            total.update(souls)

        if sort:
            total = sorted(total.items(), key=lambda pair: soulTable.index(pair[0]))

            return Counter({soul: count for soul, count in total if count > 0})

        else:
            return total
