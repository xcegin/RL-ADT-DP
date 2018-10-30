from ADT.Loops.LoopNode import LoopNode


class DoLoop(LoopNode):

    CDTName = "c.CASTDoStatement"

    def __init__(self, condition, nodeBlock):
        super().__init__(condition, nodeBlock)
        from ADT.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)
