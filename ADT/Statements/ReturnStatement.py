from ADT.Statements.StatementNode import StatementNode


class ReturnStatement(StatementNode):

    CDTName = "c.CASTReturnStatement"

    def __init__(self, id, value):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.value = resolveNodeViaType(value["$type"], value)

    def accept(self, visitor):
        return visitor.visit_statement(self)
