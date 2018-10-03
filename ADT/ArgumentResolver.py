from ADT.Statements.VariableDeclarationStatement import VariableDeclarationStatement


def resolveArguments(arguments):
    args = []
    for value in arguments["$values"]:
        variable = VariableDeclarationStatement(value["VariableTypeModifiers"], value["VariableType"],
                                                value["Variable"], value["InitialValue"])
        args.append(variable)
    return args