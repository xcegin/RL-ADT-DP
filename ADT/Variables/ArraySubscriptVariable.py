from ADT.Variables.VariableNode import VariableNode


class ArraySubscriptVariable(VariableNode):

    CDTName = "c.CASTArraySubscriptExpression"

    def __init__(self, id, variableName, array, subscript, resolverUtil, variableDeclaration=None):
        VariableNode.__init__(self, id, resolverUtil, variableName, variableDeclaration)

        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.array = resolveNodeViaType(array["$type"], array, resolverUtil)
        self.subscript = resolveNodeViaType(subscript["$type"], subscript,resolverUtil)

    def returnChildren(self):
        return super(ArraySubscriptVariable, self).returnChildren() + [self.array, self.subscript]
