from ADT.ADTNode import ADTNode
from ADT.Utils.VectorUtil import vectorizationTypeUtil


class VariableNode(ADTNode):

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __init__(self, variableName=None, variableDeclaration = None):
        self.variableName = variableName
        self.variableDeclaration = variableDeclaration

    def resolveVectorizationValue(self):
        return vectorizationTypeUtil(self.variableDeclaration.variableType.typeNode)
