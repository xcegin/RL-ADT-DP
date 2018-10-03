from ADT.ADTNode import ADTNode


class VariableDeclarationStatement(ADTNode):

    CDTName = "c.CASTDeclarationStatement"
    CDTChildFunction = "c.CASTParameterDeclaration"
    CDTChildParameter = "c.CASTSimpleDeclaration"
    CDTChildInitializer = "c.CASTEqualsInitializer"

    def __init__(self, variableTypeModifiers, variableType, variable, initialValue=None):
        self.variableTypeModifiers = variableTypeModifiers
        self.variableType = variableType
        self.variable = variable
        self.initialValue = initialValue
