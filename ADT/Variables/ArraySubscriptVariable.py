from ADT.Variables.VariableNode import VariableNode


class ArraySubscriptVariable(VariableNode):

    CDTName = "c.CASTArraySubscriptExpression"

    def __init__(self, variableName, array, subscript, variableDeclaration=None):
        VariableNode.__init__(self, variableName, variableDeclaration)

        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.array = resolveNodeViaType(array["$type"], array)
        self.subscript = resolveNodeViaType(subscript["$type"], subscript)
