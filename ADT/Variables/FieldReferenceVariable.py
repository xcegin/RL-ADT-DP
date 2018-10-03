from ADT.Variables.VariableNode import VariableNode


class FieldReferenceVariable(VariableNode):

    CDTName = "c.CASTFieldReference"
    CDTPropertyIsPointer = "PointerDereference"

    def __init__(self, variableName, variable, dereference, field):
        VariableNode.__init__(self, variableName)
        from ADT.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.dereference = dereference
        self.field = field
