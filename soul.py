from numpy import asarray, exp, sum as npSum
from numpy.random import choice
from openpyxl import load_workbook

from data import GOOD_BALANCE, PROB_PREFACTOR
from inout import writeMythical, writeSoulDict


PATH = "/Users/Ava/OneDrive/Documents/writing/Soulstones/Soulstones.xlsx"

GRIDCELLS = ('C3', 'AA27')
GRIDNAME = 'Grid'

GOODCELLS = ('I3', 'I27')
GOODNAME = 'Soulstones'

POWRCELLS = ('H3', 'H27')
POWRNAME = 'Soulstones'


def getExcel(souls: list = None,
             path: str = None,
             cellRange: tuple = None,
             gridName: str = None,
             type_: str = None):

    """ Get a dictionary from a specified Excel file. """

    assert isinstance(souls, list)
    assert all(isinstance(s, str) for s in souls)
    assert isinstance(path, str)
    assert isinstance(cellRange, tuple)
    assert len(cellRange) == 2
    assert all(isinstance(c, str) for c in cellRange)
    assert isinstance(gridName, str)
    assert isinstance(type_, str)

    start, end = cellRange

    workbook = load_workbook(filename=PATH, read_only=True, data_only=True)

    sheet = workbook.get_sheet_by_name(gridName)

    cells = sheet[start:end]

    if type_ == 'souls':
        return {motherSoul: {fatherSoul: None if cells[nM][nF].value is None else cells[nM][nF].value.lower()
                             for nF, fatherSoul in enumerate(soulTable)}
                for nM, motherSoul in enumerate(soulTable)}

    elif type_ in ('goods', 'powers'):
        return {soul: float(cells[n][0].value) for n, soul in enumerate(soulTable)}

    else:
        print(f'Do not know type {type_}. Stopping.')
        return


def getSoul(motherSoul=None, fatherSoul=None, year=None):
    """ Get the soul of a person based off parents. """

    childSoul = soulDict[motherSoul][fatherSoul]

    if childSoul in mythicals:
        writeMythical(motherSoul, fatherSoul, childSoul, year)
        return 'null'

    return childSoul


def processNulls(numNulls, souls):
    return choice(soulTable, size=numNulls, p=getSoulProbs(souls))


def getSoulProbs(souls):
    """ Determines the probabilities of picking
        each soul based on the current magical
        state of the world. """

    # Determine the good- bad- balance of the world.
    B = getBalance(souls)
    print(B)

    # Work out the probabilities of each soul based on the good/bad-ness of the world.
    probs = soulProbsArr * exp(-B * PROB_PREFACTOR
                               * asarray([goodDict[soul] - GOOD_BALANCE for soul in soulTable], dtype=float))
    print(probs)
    return probs / npSum(probs)  # Don't forget to normalise!


def getBalance(souls):
    """ Returns the magical state of the world based on
        the good- and bad- ness of the current souls. """

    return sum(goodDict[soul] * soulpowrsArr[n] * num for n, (soul, num) in enumerate(souls.items())) / sum(souls.values())


# Rarity of souls.
commons = ['null']
uncommons = ['water', 'fire', 'earth', 'wind', 'light']
rares = ['dark', 'stone', 'metal', 'flying', 'ice']
epics = ['lightning', 'poison', 'ghost', 'psychic', 'nuclear', 'gravity', 'life', 'death']
legendaries = ['soul', 'luna', 'dragon', 'dream', 'blood', 'arcane']
mythicals = ['sapphire', 'emerald', 'ruby', 'diamond', 'amethyst', 'pearl']

# Probability of falling into a rarity of soul.
probUncommon = 0.01
probRare = 0.001
probEpic = 0.0001
probLegendary = 0.00001
probMythical = 0.0
probCommon = 1.0 - probUncommon - probRare - probEpic - probLegendary - probMythical

# Probability of each soul in each rarity category.
probUncommons = [0.25, 0.25, 0.2, 0.2, 0.1]
probRares = [0.4, 0.15, 0.15, 0.15, 0.15]
probEpics = [0.2, 0.2, 0.15, 0.15, 0.1, 0.1, 0.05, 0.05]
probLegendaries = [0.2, 0.2, 0.175, 0.175, 0.125, 0.125]
probMythicals = [1.0 / 6.0] * 6
probCommons = [1.0]

# Getting the overall probability of a soul.
probUncommons = [p * probUncommon for p in probUncommons]
probRares = [p * probRare for p in probRares]
probEpics = [p * probEpic for p in probEpics]
probLegendaries = [p * probLegendary for p in probLegendaries]
probMythicals = [p * probMythical for p in probMythicals]
probCommons = [p * probCommon for p in probCommons]

# Compile probabilities together.
soulProbs = probCommons \
            + probUncommons \
            + probRares \
            + probEpics \
            + probLegendaries #\
            #+ probMythicals

# Compile souls together.
soulTable = commons\
            + uncommons\
            + rares\
            + epics\
            + legendaries #\
            #+ mythicals

soulProbsArr = asarray(soulProbs, dtype=float)

# Soul dictionary from Excel file.
soulDict = getExcel(souls=soulTable, path=PATH, cellRange=GRIDCELLS, gridName=GRIDNAME, type_='souls')
goodDict = getExcel(souls=soulTable, path=PATH, cellRange=GOODCELLS, gridName=GOODNAME, type_='goods')
#powrDict = getExcel(souls=soulTable, path=PATH, cellRange=POWRCELLS, gridName=POWRNAME, type_='powers')

# Shift good values.
goodDict = {soul: good - GOOD_BALANCE for soul, good in goodDict.items()}

# Force nulls to be exactly the desired GOOD_BALANCE.
goodDict['null'] = 0.0

'''
# Average power values.
powrAvg = sum(powrDict.values()) / len(powrDict)
powrDict = {soul: 0.0 if soul == 'null' else powr / powrAvg for soul, powr in powrDict.items()}
'''

# Define power values here.
powrCommon = 1.0
powrUncommon = 2.0
powrRare = 4.0
powrEpic = 8.0
powrLegendary = 16.0
powrMythical = 48.0

powrCommons = [1.0] * 1
powrUncommons = [1.0] * 5
powrRares = [1.0] * 5
powrEpics = [1.0] * 8
powrLegendaries = [1.0] * 6
powrMythicals = [1.0] * 6

powrCommons = [p * powrCommon for p in powrCommons]
powrUncommons = [p * powrUncommon for p in powrUncommons]
powrRares = [p * powrRare for p in powrRares]
powrEpics = [p * powrEpic for p in powrEpics]
powrLegendaries = [p * powrLegendary for p in powrLegendaries]
powrMythicals = [p * powrMythical for p in powrMythicals]

soulPowrs = powrCommons \
            + powrUncommons \
            + powrRares \
            + powrEpics \
            + powrLegendaries #\
            #+ powrMythicals

soulpowrsArr = asarray(soulPowrs, dtype=float)


writeSoulDict(soulDict)
