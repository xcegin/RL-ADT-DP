from ADT.Variables.VariableNode import VariableNode


class SimpleVariable(VariableNode):
    CDTNameInExpression = "c.CASTIdExpression"
    CDTNameInDeclaration = "c.CASTDeclarator"
    CDTNameInArray = "c.CASTArrayDeclarator"
    CDTPropertyReference = "Reference"
    CDTPropertyDefinition = "Definition"
    CDTPropertyDeclaration = "Declaration"

    def __init__(self, id, variableName, isReference, isDefinition, isDeclaration, variableDeclaration=None):
        VariableNode.__init__(self, id, variableName, variableDeclaration)
        self.isReference = isReference
        self.isDefinition = isDefinition
        self.isDeclaration = isDeclaration
