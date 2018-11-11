from ADT.Statements.StatementNode import StatementNode


class BreakStatement(StatementNode):

    CDTName = "c.CASTBreakStatement"

    def __init__(self, id):
        super().__init__(id)

    def accept(self, visitor):
        return visitor.visit_statement(self)