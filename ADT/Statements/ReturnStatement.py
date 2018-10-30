from ADT.Statements.StatementNode import StatementNode


class ReturnStatement(StatementNode):

    CDTName = "c.CASTReturnStatement"

    def __init__(self, value):
        super().__init__()
        from ADT.ResolverUtil import resolveNodeViaType
        self.value = resolveNodeViaType(value["$type"], value)

    def accept(self, visitor):
        return visitor.visit_statement(self)
