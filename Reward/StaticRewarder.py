from Reward.AbstractRewarder import Rewarder


class StaticRewardCalculator(Rewarder):

    def __init__(self):
        super().__init__()

    def resolveReward(self, currentRow, argumentValues, currentFile):
        if currentFile == 0:
            return self.resolvingCalc(currentRow, argumentValues)
        elif currentFile == 1:
            return self.resolvingNextDate(currentRow, argumentValues)

    def resolvingNextDate(self, currentRow, argumentVaues):
        def sub_resolve_0(currentRow, argumentValues):
            epR = 3
            totalR = 0
            if currentRow[0]['year LessThan 0']:
                if argumentValues['year'] < 0:
                    totalR += 1/epR
            # False 0 != a
            if not currentRow[0]['year LessThan 0']:
                if argumentValues['year'] >= 0:
                    totalR += 1/epR

            # True 0 == b
            if currentRow[1]['month LessThan 1']:
                if argumentValues['month'] < 1:
                    totalR += 1/epR

            # False 0 == b
            if not currentRow[1]['month LessThan 1']:
                if argumentValues['month'] >= 1:
                    totalR += 1/epR

            # True 1 != a
            if currentRow[2]['day LessThan 1']:
                if argumentValues['day'] < 1:
                    totalR += 1/epR

            # False 1 != a
            if not currentRow[2]['day LessThan 1']:
                if argumentValues['day'] >= 1:
                    totalR += 1/epR

            return totalR

        def sub_resolve1(currentRow, argumentValues):
            totalR = 0
            epR = 8
            if argumentValues['year'] < 0 or argumentVaues['month'] < 1 or argumentVaues['day'] < 1:
                return 0
            if currentRow[0]['yearModulus400 Equals 0']:
                if argumentValues['year'] % 400 == 0:
                    totalR += 1/epR
                # False 0 != a
            if not currentRow[0]['yearModulus400 Equals 0']:
                if argumentValues['year'] % 400 != 0:
                    totalR += 1/epR

                # True 0 == b
            if currentRow[1]['yearModulus4 Equals 0']:
                if argumentValues['year'] % 4 == 0:
                    totalR += 1/epR

                # False 0 == b
            if not currentRow[1]['yearModulus4 Equals 0']:
                if argumentValues['year'] % 4 != 0:
                    totalR += 1/epR

                # True 1 != a
            if currentRow[2]['month Equals 1']:
                if argumentValues['month'] == 1:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[2]['month Equals 1']:
                if argumentValues['month'] != 1:
                    totalR += 1/epR

            if currentRow[3]['month Equals 3']:
                if argumentValues['month'] == 3:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[3]['month Equals 3']:
                if argumentValues['month'] != 3:
                    totalR += 1/epR

            if currentRow[4]['month Equals 5']:
                if argumentValues['month'] == 5:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[4]['month Equals 5']:
                if argumentValues['month'] != 5:
                    totalR += 1/epR

            if currentRow[5]['month Equals 7']:
                if argumentValues['month'] == 7:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[5]['month Equals 7']:
                if argumentValues['month'] != 7:
                    totalR += 1/epR

            if currentRow[6]['month Equals 8']:
                if argumentValues['month'] == 8:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[6]['month Equals 8']:
                if argumentValues['month'] != 8:
                    totalR += 1/epR

            if currentRow[7]['day LessThan month_length~3']:
                month_length = self.getMeMonthLength(argumentVaues['month'], self.getMeLeapYear(argumentValues['year']))
                if argumentValues['day'] < month_length:
                    totalR += 1/epR

                # False 1 != a
            if not currentRow[7]['day LessThan month_length~3']:
                month_length = self.getMeMonthLength(argumentVaues['month'], self.getMeLeapYear(argumentValues['year']))
                if argumentValues['day'] >= month_length:
                    totalR += 1/epR

            return totalR

        def sub_resolve2(currentRow, argumentValues):
            totalR = 0
            epR = 1
            if argumentValues['year'] < 0 or argumentVaues['month'] < 1 or argumentVaues['day'] < 1:
                return 0
            if argumentValues['year'] < 0 or argumentVaues['month'] < 1 or argumentVaues['day'] < 1:
                return 0
            if currentRow[0]['yearModulus100 Equals 0']:
                if argumentValues['year'] % 100 == 0:
                    totalR += 1/epR
                # False 0 != a
            if not currentRow[0]['yearModulus100 Equals 0']:
                if argumentValues['year'] % 100 != 0:
                    totalR += 1/epR

            return totalR

        def sub_resolve3(currentRow, argumentValues):
            totalR = 0
            epR = 2
            if argumentValues['year'] < 0 or argumentVaues['month'] < 1 or argumentVaues['day'] < 1:
                return 0
            if argumentValues['month'] == 1 or argumentValues['month'] == 3 or argumentValues['month'] == 5 or argumentValues['month'] == 7 or argumentValues['month'] == 8:
                return 0
            leap_year = self.getMeLeapYear(argumentValues['year'])
            if currentRow[0]['month Equals 2']:
                if argumentValues['month'] == 2:
                    totalR += 1/epR
                # False 0 != a
            if not currentRow[0]['month Equals 2']:
                if argumentValues['month'] != 2:
                    totalR += 1/epR

            if currentRow[1]['leap_year~0 Equals 1']:
                if leap_year == 1:
                    totalR += 1/epR
                # False 0 != a
            if not currentRow[1]['leap_year~0 Equals 1']:
                if leap_year != 1:
                    totalR += 1/epR

            return totalR

        def sub_resolve4(currentRow, argumentValues):
            totalR = 0
            epR = 1
            if argumentValues['year'] < 0 or argumentVaues['month'] < 1 or argumentVaues['day'] < 1:
                return 0
            month_length = self.getMeMonthLength(argumentVaues['month'], self.getMeLeapYear(argumentValues['year']))
            if argumentValues['day'] < month_length:
                return 0
            if currentRow[0]['month Equals 12']:
                if argumentValues['month'] == 12:
                    totalR += 1/epR
                # False 0 != a
            if not currentRow[0]['month Equals 12']:
                if argumentValues['month'] != 12:
                    totalR += 1/epR

            return totalR


        if 'year LessThan 0' in currentRow[0]:
            return sub_resolve_0(currentRow, argumentVaues)
        elif 'yearModulus400 Equals 0' in currentRow[0]:
            return sub_resolve1(currentRow, argumentVaues)
        elif 'yearModulus100 Equals 0' in currentRow[0]:
            return sub_resolve2(currentRow, argumentVaues)
        elif 'month Equals 2' in currentRow[0]:
            return sub_resolve3(currentRow, argumentVaues)
        elif 'month Equals 12' in currentRow[0]:
            return sub_resolve4(currentRow, argumentVaues)


    def resolvingCalc(self, currentRow, argumentValues):
        if 'z GreaterThan x' in currentRow[0]:
            return self.sub_resolve(currentRow,argumentValues)
        eR = 0
        if (currentRow[0]['x LessThan 0'] and not currentRow[3]['x GreaterThanEquals 0']) or (not currentRow[0]['x LessThan 0'] and currentRow[3]['x GreaterThanEquals 0']):
            eR += 2
        else:
            eR += 0
        if (currentRow[1]['y LessThan 0'] and not currentRow[4]['y GreaterThanEquals 0']) or (not currentRow[1]['y LessThan 0'] and currentRow[4]['y GreaterThanEquals 0']):
            eR += 2
        else:
            eR += 0
        if (currentRow[2]['z LessThan 0'] and not currentRow[5]['z GreaterThanEquals 0']) or (not currentRow[2]['z LessThan 0'] and currentRow[5]['z GreaterThanEquals 0']):
            eR += 2
        else:
            eR += 0
        if (currentRow[6]['z Equals 0'] and currentRow[5]['z GreaterThanEquals 0'] and not currentRow[2]['z LessThan 0']) or (not currentRow[6]['z Equals 0'] and not currentRow[5]['z GreaterThanEquals 0'] and currentRow[2]['z LessThan 0']) or (not currentRow[6]['z Equals 0'] and currentRow[5]['z GreaterThanEquals 0'] and not currentRow[2]['z LessThan 0']):
            eR += 1
        totalR = 0
        # True 0 != a
        if currentRow[0]['x LessThan 0'] and not currentRow[3]['x GreaterThanEquals 0']:
            if argumentValues['x'] < 0:
                totalR += 2 / eR
        # False 0 != a
        if not currentRow[0]['x LessThan 0'] and currentRow[3]['x GreaterThanEquals 0']:
            if argumentValues['x'] >= 0:
                totalR += 2 / eR

        # True 0 == b
        if currentRow[1]['y LessThan 0'] and not currentRow[4]['y GreaterThanEquals 0']:
            if argumentValues['y'] < 0:
                totalR += 2 / eR
        # False 0 != a
        if not currentRow[1]['y LessThan 0'] and currentRow[4]['y GreaterThanEquals 0']:
            if argumentValues['y'] >= 0:
                totalR += 2 / eR

        # True 1 != a
        if currentRow[2]['z LessThan 0'] and not currentRow[5]['z GreaterThanEquals 0']:
            if argumentValues['z'] < 0:
                totalR += 2 / eR
        # False 0 != a
        if not currentRow[2]['z LessThan 0'] and currentRow[5]['z GreaterThanEquals 0']:
            if argumentValues['z'] >= 0:
                totalR += 2 / eR

        if currentRow[6]['z Equals 0'] and currentRow[5]['z GreaterThanEquals 0'] and not currentRow[2]['z LessThan 0']:
            if argumentValues['z'] == 0:
                totalR += 1 / eR

        if not currentRow[6]['z Equals 0'] and not currentRow[5]['z GreaterThanEquals 0'] and currentRow[2]['z LessThan 0']:
            if argumentValues['z'] < 0:
                totalR += 1 / eR

        if not currentRow[6]['z Equals 0'] and currentRow[5]['z GreaterThanEquals 0'] and not currentRow[2]['z LessThan 0']:
            if argumentValues['z'] > 0:
                totalR += 1 / eR

        return totalR

    def sub_resolve(self, currentRow, argumentValues):
        eR = 1
        totalR = 0
        if (currentRow[0]['z GreaterThan x'] and currentRow[2]['z GreaterThan x']) or (not currentRow[0]['z GreaterThan x'] and not currentRow[2]['z GreaterThan x']):
            eR += 2
        else:
            eR += 0
        if currentRow[0]['z GreaterThan x'] and currentRow[2]['z GreaterThan x']:
            if argumentValues['z'] > argumentValues['x']:
                totalR += 2 / eR
        # False 0 != a
        if not currentRow[0]['z GreaterThan x'] and not currentRow[2]['z GreaterThan x']:
            if argumentValues['z'] <= argumentValues['x']:
                totalR += 2 / eR

        # True 0 == b
        if currentRow[1]['z GreaterThan y']:
            if argumentValues['z'] > argumentValues['y']:
                totalR += 1 / eR
        # False 0 != a
        if not currentRow[1]['z GreaterThan y']:
            if argumentValues['z'] <= argumentValues['y']:
                totalR += 1 / eR
        return totalR

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
            if argumentValues['b'] != 0:
                totalR += 1 / 3

        # True 1 != a
        if currentRow[2]['1 NotEquals a']:
            if argumentValues['a'] != 1:
                totalR += 1 / 3

        # False 1 != a
        if not currentRow[2]['1 NotEquals a']:
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
        if currentRow[2]['c GreaterThan 5']:
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

    def onlyEntireFunctionIsCovered(self, totalR):
        if totalR == 1:
            return 1
        else:
            return 0

    def getMeLeapYear(self, year):
        if year % 400 == 0 or year % 4 == 0:
            return 1
        else:
            return 0


    def getMeMonthLength(self, month, leap_year):
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8:
                month_length = 31
        else:
            if month == 2:
                if leap_year == 1:
                    month_length = 29
                else:
                    month_length = 28
            else:
                month_length = 30
        return month_length
