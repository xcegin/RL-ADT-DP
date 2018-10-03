from ADT.ADTNode import ADTNode


class AssignmentStatement(ADTNode):

    CDTName = "c.CASTBinaryExpression"

    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
