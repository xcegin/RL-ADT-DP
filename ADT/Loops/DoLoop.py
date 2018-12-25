from ADT.Loops.LoopNode import LoopNode


class DoLoop(LoopNode):

    CDTName = "c.CASTDoStatement"

    def __init__(self, id, condition, nodeBlock, resolver_util):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition, resolver_util)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock, resolver_util)
