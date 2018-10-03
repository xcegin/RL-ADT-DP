from ADT.ADTNode import ADTNode


class AssignmentStatement(ADTNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, variable, value):
        from ADT.ResolverUtil import resolveNodeViaType
        self.variable = resolveNodeViaType(variable["$type"], variable)
        self.value = resolveNodeViaType(value["$type"], value)
