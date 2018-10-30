from ADT.Statements.StatementNode import StatementNode


class BreakStatement(StatementNode):

    CDTName = "c.CASTBreakStatement"

    def __init__(self):
        super().__init__()

    def accept(self, visitor):
        return visitor.visit_statement(self)