from ADT.Variables.VariableNode import VariableNode


class FieldReferenceVariable(VariableNode):

    CDTName = "c.CASTFieldReference"
    CDTPropertyIsPointer = "PointerDereference"

    def __init__(self, variableName, variable, dereference, field, variableDeclaration = None):
        VariableNode.__init__(self, variableName, variableDeclaration)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.dereference = dereference
        self.field = field
