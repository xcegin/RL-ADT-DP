

def resolveArguments(arguments):
    args = []
    for value in arguments["$values"]:
        from ADT.Utils.ResolverUtil import resolveNodeViaType
        variable = resolveNodeViaType(value["$type"], value)
        args.append(variable)
    return args