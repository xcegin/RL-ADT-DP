from ADT.ArgumentResolver import resolveArguments
from ADT.Statements.StatementNode import StatementNode


class FunctionDeclarationStatement(StatementNode):

    CDTName = "c.CASTFunctionDefinition"
    CDTChildFunction = "c.CASTFunctionDeclarator"
    CDTChildParameter = "c.CASTParameterDeclaration"

    def __init__(self, returnType, name, arguments, body):
        super().__init__()
        self.name = name
        self.arguments = resolveArguments(arguments)
        from ADT.ResolverUtil import resolveNodeViaType
        self.returnType = resolveNodeViaType(returnType["$type"], returnType)
        self.body = resolveNodeViaType(body["$type"], body["Nodes"])

    def accept(self, visitor):
        return visitor.visit_functiondeclaration(self)