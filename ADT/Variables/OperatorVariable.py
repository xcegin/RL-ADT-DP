from ADT.Variables.VariableNode import VariableNode


class OperatorVariable(VariableNode):

    def __init__(self, variableName, operator):
        VariableNode.__init__(self, variableName)
        from ADT.ResolverUtil import resolveNodeViaType
        self.operator = resolveNodeViaType(operator["$type"], operator)
