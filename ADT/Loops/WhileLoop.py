from ADT.Loops.LoopNode import LoopNode


class WhileLoop(LoopNode):

    CDTName = "c.CASTWhileStatement"

    def __init__(self, id, condition, nodeBlock):
        super().__init__(id, condition, nodeBlock)
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        self.condition = resolveNodeViaType(condition["$type"], condition)
        self.nodeBlock = resolveNodeViaType(nodeBlock["$type"], nodeBlock)
