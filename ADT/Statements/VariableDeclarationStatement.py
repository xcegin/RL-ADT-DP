from ADT.Statements.StatementNode import StatementNode


class VariableDeclarationStatement(StatementNode):

    CDTName = "c.CASTDeclarationStatement"
    CDTChildFunction = "c.CASTParameterDeclaration"
    CDTChildParameter = "c.CASTSimpleDeclaration"
    CDTChildInitializer = "c.CASTEqualsInitializer"

    def __init__(self, id, variableType, initialValue=None):
        super().__init__(id)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        if variableType is None:
            from ADT.UnknowNode import UnknownNode
            self.variableType = UnknownNode("unknown")
        else:
            self.variableType = resolveNodeViaType(variableType["$type"], variableType)
        self.variable = None
        self.initialValue = initialValue

    def accept(self, visitor):
        return visitor.visit_variabledeclaration(self)
