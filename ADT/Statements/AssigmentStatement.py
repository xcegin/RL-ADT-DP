from ADT.Statements.StatementNode import StatementNode


class AssignmentStatement(StatementNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, variable, value):
        super().__init__()
        from ADT.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.value = resolveNodeViaType(value["$type"], value)

    def accept(self, visitor):
        return visitor.visit_assigment(self)