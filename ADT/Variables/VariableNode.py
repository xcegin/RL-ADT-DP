from ADT.ADTNode import ADTNode
from ADT.Utils.VectorUtil import vectorizationTypeUtil


class VariableNode(ADTNode):

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __init__(self, id, variableName=None, variableDeclaration=None):
        super().__init__(id)
        self.variableName = variableName
        self.variableDeclaration = variableDeclaration

    def resolveVectorizationValue(self):
        return vectorizationTypeUtil(self.variableDeclaration.variableType.typeName)
