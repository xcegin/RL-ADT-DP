def resolveHeuristic(currentRow, argumentValues, currentFile):
    if currentFile == 0:
        return resolving0(currentRow, argumentValues)
    elif currentFile == 1:
        return resolving1(currentRow, argumentValues)
    elif currentFile == 2:
        return resolving2(currentRow, argumentValues)
    elif currentFile == 3:
        return simple(currentRow, argumentValues)


def resolving0(currentRow, argumentValues):
    totalR = 0
    # True 0 != a
    if currentRow[0]['0 NotEquals a']:
        if argumentValues['a'] != 0:
            totalR += 1 / 3
    # False 0 != a
    if not currentRow[0]['0 NotEquals a']:
        if argumentValues['a'] == 0:
            totalR += 1 / 3

    # True 0 == b
    if currentRow[0]['0 Equals b']:
        if argumentValues['b'] == 0:
            totalR += 1 / 3

    # False 0 == b
    if not currentRow[0]['0 Equals b']:
        if argumentValues['a'] != 0:
            totalR += 1 / 3

    # True 1 != a
    if currentRow[0]['1 NotEquals a']:
        if argumentValues['a'] != 1:
            totalR += 1 / 3

    # False 1 != a
    if currentRow[0]['1 NotEquals a']:
        if argumentValues['a'] == 1:
            totalR += 1 / 3

    return totalR

def resolving1(currentRow, argumentValues):
    totalR = 0
    # True z & 1
    if currentRow[0]['zAnd1']:
        if argumentValues['z'] == 1:
            totalR += 1
    # False z & 1
    if not currentRow[0]['zAnd1']:
        if argumentValues['a'] != 0:
            totalR += 1
    return totalR

def resolving2(currentRow, argumentValues):
    totalR = 0
    # True 0 != a
    if currentRow[0]['0 NotEquals a']:
        if argumentValues['a'] != 0:
            totalR += 1 / 3
    # False 0 != a
    if not currentRow[0]['0 NotEquals a']:
        if argumentValues['a'] == 0:
            totalR += 1 / 3

    # True 0 == b
    if currentRow[0]['0 Equals b']:
        if argumentValues['b'] == 0:
            totalR += 1 / 3

    # False 0 == b
    if not currentRow[0]['0 Equals b']:
        if argumentValues['a'] != 0:
            totalR += 1 / 3

    # True c > 5
    if not currentRow[0]['c GreaterThan 5']:
        if argumentValues['c'] > 5:
            totalR += 1 / 3

    # False c > 5
    if not currentRow[0]['c GreaterThan 5']:
        if argumentValues['c'] < 5:
            totalR += 1 / 3

    return totalR


def simple(currentRow, argumentValues):
    totalR = 0
    # True a < b
    if currentRow[0]['a LessThanEquals b']:
        if argumentValues['a'] <= argumentValues['b']:
            totalR += 1
    # False a < b
    if not currentRow[0]['0 NotEquals a']:
        if argumentValues['a'] > argumentValues['b']:
            totalR += 1
    return totalR
