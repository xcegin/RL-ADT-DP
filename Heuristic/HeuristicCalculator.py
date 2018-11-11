class HeuristicCalculator:
    def __init__(self):
        super()

    def calculateHeuristicFerOneFeckinRowM8(self, oneFeckinRow):
        finalShait = ""
        for simpleExpression in oneFeckinRow:
            token = list(simpleExpression)[0]
            if finalShait == "":
                finalShait += self.resolveOneExpressions(token, simpleExpression[token])
            else:
                finalShait += " + " + self.resolveOneExpressions(token, simpleExpression[token])
        return finalShait

    def resolveOneExpressions(self, token, truthValue):
        splitToken = token.split(" ")
        tmpList = []
        for token in splitToken:
            if "~" in token:
                tmpList.append(self.replaceTildeVariableNames(token))
            else:
                tmpList.append(token)
        splitToken = tmpList

        if (splitToken[1] == "Equals" and truthValue) or (splitToken[1] == "NotEquals" and not truthValue):
            return "abs(" + splitToken[0] + " - " + splitToken[2] + ")"
        elif (splitToken[1] == "Equals" and not truthValue) or (splitToken[1] == "NotEquals" and truthValue):
            return "small(" + splitToken[0] + ")"
        elif (splitToken[1] == "LessThan" and truthValue) or (splitToken[1] == "LessThanEquals" and not truthValue):
            return "abs(" + splitToken[0] + " - " + splitToken[2] + ")"
        elif (splitToken[1] == "LessThan" and not truthValue) or (splitToken[1] == "LessThanEquals" and truthValue):
            return "abs(" + splitToken[0] + " - " + splitToken[2] + ")" + " + " + "small(" + splitToken[0] + ")"
        elif (splitToken[1] == "GreaterThan" and truthValue) or (
                splitToken[1] == "GreaterThanEquals" and not truthValue):
            return "abs(" + splitToken[0] + " - " + splitToken[2] + ")"
        elif (splitToken[1] == "GreaterThan" and not truthValue) or (
                splitToken[1] == "GreaterThanEquals" and truthValue):
            return "abs(" + splitToken[0] + " - " + splitToken[2] + ")" + " + " + "small(" + splitToken[0] + ")"
        # TODO resolve And & Or
        else:
            return "min(" + splitToken[0] + " - " + splitToken[2] + ")"

    def replaceTildeVariableNames(self, key):
        indexOfTilde = key.find("~")
        tmp = key[indexOfTilde:]
        indexOfSpace = tmp.find(" ")
        newKey = key[:indexOfTilde] + tmp[indexOfSpace:]
        if "~" in newKey:
            return self.replaceTildeVariableNames(newKey)
        return newKey[:-1]