from ADT.ADTNode import ADTNode


class VariableDeclarationStatement(ADTNode):

    CDTName = "c.CASTDeclarationStatement"
    CDTChildFunction = "c.CASTParameterDeclaration"
    CDTChildParameter = "c.CASTSimpleDeclaration"
    CDTChildInitializer = "c.CASTEqualsInitializer"

    def __init__(self, variableTypeModifiers, variableType, variable, initialValue=None):
        self.variableTypeModifiers = variableTypeModifiers
        self.variableType = variableType
        from ADT.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.initialValue = initialValue
