from ADT.Statements.StatementNode import StatementNode
from ADT.Variables.VariableNode import VariableNode


class AssignmentStatement(StatementNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, variable, value):
        super().__init__()
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.value = resolveNodeViaType(value["$type"], value)

    def accept(self, visitor):
        return visitor.visit_assigment(self)

    #TODO Calculate the aproximate complexity of assigment statement -> thus how complex is the expression
    def return_vector(self, visitor):
        list = []
        if self.variable is VariableNode:
            visitor.currentArgumentVectorDependency = self.variable.variableName
            list.append(self.value.accept(visitor))
        return list