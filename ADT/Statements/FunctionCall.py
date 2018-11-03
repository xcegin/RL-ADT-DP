# TODO: This should be replaced with an entire ADT structure of the called function
from ADT.Statements.StatementNode import StatementNode


class FunctionCall(StatementNode):
    CDTName = "c.CASTFunctionCallExpression"
    CDTChildFunction = "c.CASTIdExpression"

    def __init__(self, name, arguments):
        super().__init__()
        self.name = name
        from ADT.Utils.ArgumentResolver import resolveArguments
        self.arguments = resolveArguments(arguments)

    def accept(self, visitor):
        return visitor.visit_functioncall(self)

    def resolveVectorizationValue(self):
        return 0