# TODO should be all the variables, not just the arguments for the small operation, abs is fine propably ->
# TODO ideally track data dependencies
from ADT.Utils.MathOperationsUtil import smallestValue
from Reward.AbstractRewarder import Rewarder


class HeuristicRewarder(Rewarder):

    def __init__(self):
        super().__init__()

    def resolveReward(self, valuesOfArguments, arguments, heuristic):

        def replaceTokensForArgs(token1, token2):
            tok1, tok2 = token1, token2
            if token1 in arguments:
                tok1 = valuesOfArguments[token1]
            if token2 in arguments:
                tok2 = valuesOfArguments[token2]
            return float(tok1), float(tok2)

        componentOfHeuristic = heuristic[0].split("+")
        numOfPossibleRewards = len(componentOfHeuristic)
        finalValue = 0
        for component in componentOfHeuristic:
            if component == '1':
                return 1
            if component == '0':
                return 0
            tokens = component.split(" ")
            if tokens[1] == "Equals":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] == tokens[2]:
                    finalValue += 1/numOfPossibleRewards
            elif tokens[1] == "NotEquals":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] != tokens[2]:
                    finalValue += 1/numOfPossibleRewards
            elif tokens[1] == "LessThan":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] < tokens[2]:
                    finalValue += 1/numOfPossibleRewards
            elif tokens[1] == "GreaterThanEquals":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] >= tokens[2]:
                    finalValue += 1/numOfPossibleRewards
            elif tokens[1] == "GreaterThan":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] > tokens[2]:
                    finalValue += 1/numOfPossibleRewards
            elif tokens[1] == "LessThanEquals":
                tokens[0], tokens[2] = replaceTokensForArgs(tokens[0], tokens[2])
                if tokens[0] <= tokens[2]:
                    finalValue += 1/numOfPossibleRewards
        return finalValue


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
