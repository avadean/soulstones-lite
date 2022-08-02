from collections import Counter


def writeInit(population):
    with open('init.dat', 'w') as fileInit:
        fileInit.write(f'{str(population)}\n')


def writeSoulDict(soulDict: dict = None):
    with open('soulDict.dat', 'w') as fileSoulDict:
        fileSoulDict.write('  motherSoul +  fatherSoul  = childSoul  \n')
        fileSoulDict.write('-----------------------------------------\n')
        for mSoul, fSoulDict in soulDict.items():
            for fSoul, cSoul in fSoulDict.items():
                fileSoulDict.write(f'{str(mSoul):>12} + {str(fSoul):^12} = {str(cSoul):<12}\n')


def writeMythical(mSoul: str = None, fSoul: str = None, cSoul: str = None, year: int = None):
    with open('mythicals.dat', 'a') as fileMythicals:
        fileMythicals.write(f'{mSoul:>12} + {fSoul:^12} = {cSoul:<12} ... in year {year}\n')


def writeSummary(souls: Counter = None, index: int = None):
    index = '' if index is None else f'{index}'

    cTotal = sum(souls.values())

    if cTotal == 0:
        print('No summary written.')
        return

    with open(f'summary{index}.dat', 'w') as fileSummary:
        cNull = souls['null']

        fileSummary.write('/==================================================\\\n')
        fileSummary.write(f'|{"total":>12} : {cTotal:>7}                            |\n')
        fileSummary.write('|                                                  |\n')
        fileSummary.write(f'|{"null":>12} : {cNull:>7}    {100.0 * cNull / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|==================================================|\n')

        cMagical = sum(souls.values()) - cNull

        if cMagical == 0:
            print('No magical written.')
            return

        fileSummary.write(f'|{"magical":>12} : {cMagical:>7}    {100.0 * cMagical / cTotal:8.3f} % of total     |\n')
        fileSummary.write('|                                                  |\n')

        for soul, cSoul in souls.items():
            if soul == 'null':
                continue

            fileSummary.write(f'|{soul:>12} : {cSoul:>7}    {100.0 * cSoul / cMagical:8.3f} % of magical   |\n')

        fileSummary.write('\\==================================================/')
