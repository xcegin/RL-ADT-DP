from ADT.Statements.StatementNode import StatementNode


class ReturnStatement(StatementNode):

    CDTName = "c.CASTReturnStatement"

    def __init__(self, id, value, resolverUtil):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.value = resolveNodeViaType(value["$type"], value, resolverUtil)

    def accept(self, visitor):
        return visitor.visit_statement(self)

    def returnChildren(self):
        return [self.value]
