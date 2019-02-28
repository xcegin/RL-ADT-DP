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
                finalShait += "+" + self.resolveOneExpressions(token, simpleExpression[token])
        return finalShait

    def resolveOneExpressions(self, token, truthValue):
        if token == '1' or token == '0':
            return '1'
        if "And" in token:
            token = token.replace("And", " And ")
        if "Or" in token:
            token = token.replace("Or", " Or ")
        splitToken = token.split(" ")
        tmpList = []
        for stoken in splitToken:
            if "~" in stoken:
                tmpList.append(self.replaceTildeVariableNames(stoken))
            else:
                tmpList.append(stoken)
        splitToken = tmpList

        if (splitToken[1] == "Equals" and truthValue) or (splitToken[1] == "NotEquals" and not truthValue):
            return splitToken[0] + " Equals " + splitToken[2]
        elif (splitToken[1] == "Equals" and not truthValue) or (splitToken[1] == "NotEquals" and truthValue):
            return splitToken[0] + " NotEquals " + splitToken[2]
        elif (splitToken[1] == "LessThan" and truthValue) or (splitToken[1] == "GreaterThanEquals" and not truthValue):
             return splitToken[0] + " LessThan " + splitToken[2]
        elif (splitToken[1] == "LessThan" and not truthValue) or (splitToken[1] == "GreaterThanEquals" and truthValue):
            return splitToken[0] + " GreaterThanEquals " + splitToken[2]
        elif (splitToken[1] == "GreaterThan" and truthValue) or (
                splitToken[1] == "LessThanEquals" and not truthValue):
            return splitToken[0] + " GreaterThan " + splitToken[2]
        elif (splitToken[1] == "GreaterThan" and not truthValue) or (
                splitToken[1] == "LessThanEquals" and truthValue):
            return splitToken[0] + " LessThanEquals " + splitToken[2]
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