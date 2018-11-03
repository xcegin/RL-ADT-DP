from ADT.Statements.StatementNode import StatementNode


class VariableDeclarationStatement(StatementNode):

    CDTName = "c.CASTDeclarationStatement"
    CDTChildFunction = "c.CASTParameterDeclaration"
    CDTChildParameter = "c.CASTSimpleDeclaration"
    CDTChildInitializer = "c.CASTEqualsInitializer"

    def __init__(self, variableType, initialValue=None):
        super().__init__()
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variableType = resolveNodeViaType(variableType["$type"], variableType)
        self.variable = None
        self.initialValue = initialValue

    def accept(self, visitor):
        return visitor.visit_variabledeclaration(self)
