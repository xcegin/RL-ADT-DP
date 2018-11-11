from ADT.Loops.LoopNode import LoopNode


class DoLoop(LoopNode):

    CDTName = "c.CASTDoStatement"

    def __init__(self, id, condition, nodeBlock):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)
