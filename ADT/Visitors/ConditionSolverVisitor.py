from Enviroment import Utils
from Enviroment.Utils import getTypeOfExpression

space = " "
leftBracket = "("
rightBracket = ")"


class ConditionSolverVisitor:

    def __init__(self, expression, rowExpressionValues, expressions):
        self.expressions = expressions
        self.simpleExpressions = []
        self.expressionToken = expression["Token"]
        self.expression = expression
        self.rowExpressionValues = rowExpressionValues
        self.isRoot = True

    def retrieveValueOfCondition(self):
        expressions = []
        self.retrieveExpressions(self.expression["Children"]["$values"], expressions)
        for expression in expressions:
            self.expressionToken = self.expressionToken.replace(expression,
                                                                        str(self.rowExpressionValues[expression]))
        self.expressionToken = self.expressionToken.replace("And", "and")
        self.expressionToken = self.expressionToken.replace("Or", "or")
        return eval(self.expressionToken)

    def retrieveExpressions(self, values, expressions):
        for expression in values:
            if getTypeOfExpression(expression["$type"]) == Utils.COMPOSITE_EXPRESSION:
                self.retrieveExpressions(expression["Children"]["$values"], expressions)
            else:
                expressions.append(expression["Token"])
        return expressions