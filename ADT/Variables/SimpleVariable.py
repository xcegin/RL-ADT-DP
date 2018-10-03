from ADT.Variables.VariableNode import VariableNode


class SimpleVariable(VariableNode):
    CDTNameInExpression = "c.CASTIdExpression"
    CDTNameInDeclaration = "c.CASTDeclarator"
    CDTNameInArray = "c.CASTArrayDeclarator"
    CDTPropertyReference = "Reference"
    CDTPropertyDefinition = "Definition"
    CDTPropertyDeclaration = "Declaration"

    def __init__(self, variableName, isReference, isDefinition, isDeclaration):
        VariableNode.__init__(self, variableName)
        self.isReference = isReference
        self.isDefinition = isDefinition
        self.isDeclaration = isDeclaration
