from ADT.ADTNode import ADTNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement
from ADT.Utils.VectorUtil import vectorizationTypeUtil


class VariableNode(ADTNode):

    def accept(self, visitor):
        return visitor.visit_variable(self)

    def __init__(self, id, resolverUtil, variableName=None, variableDeclaration=None):
        super().__init__(id)
        self.variableName = variableName
        if variableDeclaration is not None:
            if isinstance(variableDeclaration, VariableDeclarationStatement):
                self.variableDeclaration = variableDeclaration
            else:
                from ADT.Utils.ResolverUtil import resolveNodeViaType
                self.variableDeclaration = resolveNodeViaType(variableDeclaration["$type"], variableDeclaration, resolverUtil)
        else:
            self.variableDeclaration = None
        self.variableDeclaration = variableDeclaration

    def resolveVectorizationValue(self):
        return vectorizationTypeUtil(self.variableDeclaration.variableType.typeName)

    def returnChildren(self):
        return []
