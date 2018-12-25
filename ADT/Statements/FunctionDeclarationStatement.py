from ADT.Utils.ArgumentResolver import resolveArguments
from ADT.Statements.StatementNode import StatementNode


class FunctionDeclarationStatement(StatementNode):

    CDTName = "c.CASTFunctionDefinition"
    CDTChildFunction = "c.CASTFunctionDeclarator"
    CDTChildParameter = "c.CASTParameterDeclaration"

    def __init__(self, id, returnType, name, arguments, body, resolverUtil):
        super().__init__(id)
        self.name = name
        self.arguments = resolveArguments(arguments, resolverUtil)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.returnType = resolveNodeViaType(returnType["$type"], returnType, resolverUtil)
        self.body = resolveNodeViaType(body["$type"], body["Nodes"], resolverUtil)

    def accept(self, visitor):
        return visitor.visit_functiondeclaration(self)