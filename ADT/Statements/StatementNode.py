from ADT.ADTNode import ADTNode


class StatementNode(ADTNode):

    def accept(self,  visitor):
        pass

    def __init__(self, id):
        super().__init__(id)

    def resolveVectorizationValue(self):
        return 0
