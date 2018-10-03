from ADT.ADTNode import ADTNode


class FunctionCall(ADTNode):

    CDTName = "c.CASTFunctionCallExpression"
    CDTChildFunction =  "c.CASTIdExpression"

    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments
