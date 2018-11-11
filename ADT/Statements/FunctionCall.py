from ADT.Statements.StatementNode import StatementNode


class FunctionCall(StatementNode):
    CDTName = "c.CASTFunctionCallExpression"
    CDTChildFunction = "c.CASTIdExpression"

    def __init__(self, id, name, arguments, declaration):
        super().__init__(id)
        self.name = name
        from ADT.Utils.ArgumentResolver import resolveArguments
        self.arguments = resolveArguments(arguments)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        # TODO: Replace entire tree with variables from arguments.. also if there exist variables with this name in the body of the function - replace it
        if declaration is None:
            from ADT.UnknowNode import UnknownNode
            self.functionDeclaration = UnknownNode("unknown")
        else:
            self.functionDeclaration = resolveNodeViaType(declaration["$type"], declaration)

    def accept(self, visitor):
        return visitor.visit_functioncall(self)

    def resolveVectorizationValue(self):
        return 0