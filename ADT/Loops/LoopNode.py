from ADT.ADTNode import ADTNode


class LoopNode(ADTNode):

    def __init__(self, condition, nodeBlock):
        self.condition = condition
        self.nodeBlock = nodeBlock

    def accept(self, visitor):
        return visitor.visit_loop(self)