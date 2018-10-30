from ADT.ADTNode import ADTNode


class UnknownNode(ADTNode):

    def __init__(self):
        pass

    def accept(self, visitor):
        return visitor.visit_unknown(self)
