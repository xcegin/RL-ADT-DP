from ADT.ADTNode import ADTNode


class ReturnStatement(ADTNode):

    CDTName = "c.CASTReturnStatement"

    def __init__(self, value):
        from ADT.ResolverUtil import resolveNodeViaType
        self.value = resolveNodeViaType(value["$type"], value)
