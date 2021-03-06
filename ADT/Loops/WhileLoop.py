from ADT.Loops.LoopNode import LoopNode


class WhileLoop(LoopNode):

    CDTName = "c.CASTWhileStatement"

    def __init__(self, id, condition, nodeBlock, resolver_util):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition, resolver_util)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock, resolver_util)
