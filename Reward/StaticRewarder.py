from Reward.AbstractRewarder import Rewarder


class StaticRewardCalculator(Rewarder):

    def __init__(self):
        super().__init__()

    def resolveReward(self, currentRow, argumentValues, currentFile):
        if currentFile == 0:
            return self.resolving0(currentRow, argumentValues)
        elif currentFile == 1:
            return self.resolving1(currentRow, argumentValues)
        elif currentFile == 2:
            return self.resolving2(currentRow, argumentValues)
        elif currentFile == 3:
            return self.simple(currentRow, argumentValues)

    def resolving0(self, currentRow, argumentValues):
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
        if currentRow[1]['0 Equals b']:
            if argumentValues['b'] == 0:
                totalR += 1 / 3

        # False 0 == b
        if not currentRow[1]['0 Equals b']:
            if argumentValues['a'] != 0:
                totalR += 1 / 3

        # True 1 != a
        if currentRow[2]['1 NotEquals a']:
            if argumentValues['a'] != 1:
                totalR += 1 / 3

        # False 1 != a
        if currentRow[2]['1 NotEquals a']:
            if argumentValues['a'] == 1:
                totalR += 1 / 3

        return totalR

    def resolving1(self, currentRow, argumentValues):
        totalR = 0
        # True z & 1
        if currentRow[0]['zAnd1']:
            if argumentValues['a'] == 1:
                totalR += 1
        # False z & 1
        if not currentRow[0]['zAnd1']:
            if argumentValues['a'] != 0:
                totalR += 1
        return totalR

    def resolving2(self, currentRow, argumentValues):
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
        if currentRow[1]['0 Equals b']:
            if argumentValues['b'] == 0:
                totalR += 1 / 3

        # False 0 == b
        if not currentRow[1]['0 Equals b']:
            if argumentValues['a'] != 0:
                totalR += 1 / 3

        # True c > 5
        if not currentRow[2]['c GreaterThan 5']:
            if argumentValues['c'] > 5:
                totalR += 1 / 3

        # False c > 5
        if not currentRow[2]['c GreaterThan 5']:
            if argumentValues['c'] < 5:
                totalR += 1 / 3

        return totalR

    def simple(self, currentRow, argumentValues):
        totalR = 0
        # True a < b
        if currentRow[0]['a LessThanEquals b']:
            if argumentValues['a'] <= argumentValues['b']:
                totalR += 1
        # False a < b
        if not currentRow[0]['a LessThanEquals b']:
            if argumentValues['a'] > argumentValues['b']:
                totalR += 1
        return totalR
