from ADT.Variables.VariableNode import VariableNode


class OperatorVariable(VariableNode):

    def __init__(self, variableName, operator, variableDeclaration=None):
        VariableNode.__init__(self, variableName, variableDeclaration)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.operator = resolveNodeViaType(operator["$type"], operator)
