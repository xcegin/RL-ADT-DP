from ADT.Variables.VariableNode import VariableNode


class OperatorVariable(VariableNode):

    def __init__(self, id, variableName, operator, resolverUtil, variableDeclaration=None):
        VariableNode.__init__(self, id, resolverUtil, variableName, variableDeclaration)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.operator = resolveNodeViaType(operator["$type"], operator, resolverUtil)

    def returnChildren(self):
        return super(OperatorVariable, self).returnChildren() + [self.operator]