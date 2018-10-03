from ADT.ADTNode import ADTNode


class ReturnStatement(ADTNode):

    CDTName = "c.CASTReturnStatement"

    def __init__(self, value):
        self.value = value
