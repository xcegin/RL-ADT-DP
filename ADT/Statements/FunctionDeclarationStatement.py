from ADT.ADTNode import ADTNode
from ADT.SequenceNode import SequenceNode
from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement


class FunctionDeclarationStatement(ADTNode):

    CDTName = "c.CASTFunctionDefinition"
    CDTChildFunction = "c.CASTFunctionDeclarator"
    CDTChildParameter = "c.CASTParameterDeclaration"

    def __init__(self, returnTypeModifiers, returnType, name, arguments, body):
        self.returnTypeModifiers = returnTypeModifiers
        self.returnType = returnType
        self.name = name
        self.arguments = self.resolveArguments(arguments)
        self.body = SequenceNode(body["Nodes"])

    def resolveArguments(self, arguments):
        args = []
        for value in arguments["$values"]:
            variable = VariableDeclarationStatement(value["VariableTypeModifiers"], value["VariableType"],
                                                    value["Variable"], value["InitialValue"])
            args.append(variable)
        return args
