from ADT.ADTNode import ADTNode


class UnknownNode(ADTNode):

    def __init__(self, id):
        super().__init__(id)

    def accept(self, visitor):
        return visitor.visit_unknown(self)

    def resolveVectorizationValue(self):
        return -1