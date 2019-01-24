from ADT.Variables.VariableNode import VariableNode


class FieldReferenceVariable(VariableNode):

    CDTName = "c.CASTFieldReference"
    CDTPropertyIsPointer = "PointerDereference"

    def __init__(self, id, variableName, variable, dereference, field, resolverUtil, variableDeclaration = None):
        VariableNode.__init__(self, id, resolverUtil, variableName, variableDeclaration)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable, resolverUtil)
        self.dereference = dereference
        self.field = field

    def returnChildren(self):
        return super(FieldReferenceVariable, self).returnChildren() + [self.variable]
